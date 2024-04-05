import asyncio
import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from googleapiclient.errors import HttpError

from UI.buttons.data_buttons import admin_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from database.database_config import database_name, table_queries, table_workers
from database.enums import WorkerField
from database.enums.query_field import QueryType, QueryField
from filters import IsAdmin, IsPrivate
from google_sheets.methods import create_new_timetable, write_timetable
from loader import bot
from utils import sql, make_form


class CoordinationTimetables(StatesGroup):
    coordination = State()
    rejection = State()


router = Router()


async def get_queries():
    return await sql.select(
        database_name,
        table_queries,
        f"{QueryField.TYPE.value} = ?",
        (QueryType.SENDING_TIMETABLE.value,)
    )


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.COORDINATE_TIMETABLES.value)
async def coordinate_timetables(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    queries = await get_queries()

    if await has_pending_queries(queries, callback_query.message, state):
        await state.update_data(queries=queries)
        await show_next_timetable(callback_query.message, state)
        await state.set_state(CoordinationTimetables.coordination)


async def has_pending_queries(queries: list, message: types.Message, state: FSMContext):
    if len(queries) == 0:
        await message.answer("Пока запросов нет")
        await show_main_menu(message, admin_buttons)
        await state.clear()
        return False
    return True


async def extract_query_data(queries):
    if len(queries) == 0:
        return None

    query_id, worker_id, query_type, query_text = queries.pop(0)
    return {
        QueryField.ID.value: query_id,
        QueryField.WORKER_ID.value: worker_id,
        QueryField.TYPE.value: query_type,
        QueryField.QUERY_TEXT.value: query_text
    }


async def get_worker_data(worker_id: int):
    return await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.ID.value} = ?",
        (worker_id,),
        [WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID]
    )


@router.message(StateFilter(CoordinationTimetables.coordination), IsAdmin())
async def show_next_timetable(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    queries = user_data["queries"]
    if await has_pending_queries(queries, message, state):
        query_data = await extract_query_data(queries)
        worker_data = await get_worker_data(query_data[QueryField.WORKER_ID.value])
        full_name, user_id = worker_data[0]
        await state.update_data({
            "query_data": query_data,
            WorkerField.TELEGRAM_ID.value: user_id,
            WorkerField.FULL_NAME.value: full_name
        })
        await message.answer(
            await make_form_for_coordination_timetable(
                json.loads(query_data[QueryField.QUERY_TEXT.value]),
                full_name),
            reply_markup=await make_inline_keyboard([OtherButton.REJECT.value, OtherButton.ACCEPT.value]),
            parse_mode="HTML"
        )
        await state.set_state(CoordinationTimetables.coordination)


async def make_form_for_coordination_timetable(timetable: dict, full_name: str):
    form = await make_form(timetable)
    return f"Расписание сотрудника {full_name}:\n\n<pre>{form}</pre>"


@router.callback_query(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin(),
    F.data == OtherButton.ACCEPT.value
)
async def accept_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    timetable: dict = json.loads(user_data["query_data"][QueryField.QUERY_TEXT.value])
    await set_timetable_in_spread_sheet(user_data, timetable)
    await callback_query.message.edit_text("Вы приняли расписание...")
    await bot.send_message(user_data[WorkerField.TELEGRAM_ID.value], f"Ваше расписание принято!")
    await delete_query(callback_query.message, state)


async def set_timetable_in_spread_sheet(user_data, timetable: dict):
    try:
        await write_timetable(constants.NEW_TIMETABLE, timetable, user_data)
    except Exception as error:
        await asyncio.sleep(1)
        try:
            await create_new_timetable(constants.NEW_TIMETABLE)
        except Exception as error:
            print(isinstance(error, HttpError))
        await set_timetable_in_spread_sheet(user_data, timetable)


@router.callback_query(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin(),
    F.data == OtherButton.REJECT.value
)
async def reject_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Напишите причину отказа")
    await state.set_state(CoordinationTimetables.rejection)


@router.message(
    IsPrivate(),
    StateFilter(CoordinationTimetables.rejection),
    IsAdmin()
)
async def take_rejection_reason(message: types.Message, state: FSMContext):
    await message.answer("Причина отказа отправлена...")
    user_data = await state.get_data()
    user_id = user_data[WorkerField.TELEGRAM_ID.value]
    await bot.send_message(user_id, f"Ваше расписание отклонено по причине: {message.text}")
    await delete_query(message, state)


async def delete_query(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    query_id = user_data["query_data"][QueryField.ID.value]
    await sql.delete(
        database_name,
        table_queries,
        f"{QueryField.ID.value} = ?",
        (query_id,))
    await show_next_timetable(message, state)
