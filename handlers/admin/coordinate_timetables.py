import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from UI.buttons.data_buttons import admin_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from data.config import SPREADSHEET_ID
from database.database_config import database_name, table_queries, table_workers
from database.enums import WorkerField
from database.enums.query_field import QueryType, QueryField
from filters import IsAdmin
from google_sheets import service
from handlers.worker.make_timetable import get_number_hours
from loader import bot
from utils import sql


class CoordinationTimetables(StatesGroup):
    coordination = State()
    rejection = State()


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.COORDINATE_TIMETABLES.value)
async def coordinate_timetables(callback_query: types.CallbackQuery, state: FSMContext):
    queries = await sql.select(
        database_name,
        table_queries,
        f"{QueryField.TYPE.value} = ?",
        QueryType.MAKING_TIMETABLE_BY_WORKER.value
    )

    if len(queries) == 0:
        await callback_query.message.answer("Пока запросов нет")
        await show_main_menu(callback_query.message, admin_buttons)
        await state.clear()
        return

    await state.update_data(queries=queries)
    await show_next_timetable(callback_query.message, state)
    await state.set_state(CoordinationTimetables.coordination)


@router.message(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin()
)
async def show_next_timetable(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    queries: list = user_data["queries"]
    if len(queries) == 0:
        await message.answer("Пока запросов нет")
        await show_main_menu(message, admin_buttons)
        await state.clear()
        return

    query_id, worker_id, query_type, query_text = queries.pop(0)
    await state.update_data(
        {
            f"{QueryField.ID.value}": query_id,
            f"{QueryField.USER_ID.value}": worker_id,
            f"{QueryField.TYPE.value}": query_type,
            f"{QueryField.QUERY_TEXT.value}": query_text,
        }
    )
    await message.answer(
        query_text,
        reply_markup=await make_inline_keyboard([OtherButton.REJECT.value, OtherButton.ACCEPT.value])
    )

    await state.set_state(CoordinationTimetables.coordination)


@router.callback_query(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin(),
    F.data == OtherButton.REJECT.value
)
async def reject_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Напишите причину отказа")
    await state.set_state(CoordinationTimetables.rejection)


@router.callback_query(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin(),
    F.data == OtherButton.ACCEPT.value
)
async def accept_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback_query.message.edit_text("Вы приняли расписание...")
    timetable: dict = json.loads(user_data[f"{QueryField.QUERY_TEXT.value}"])
    await set_timetable_in_spread_sheet(user_data, timetable)

    id_worker = user_data[f"{QueryField.USER_ID.value}"]
    await bot.send_message(id_worker, f"Ваше расписание принято!")
    await delete_query(callback_query.message, state)


async def set_timetable_in_spread_sheet(user_data, timetable: dict):
    name_sheet = "Новое расписание"
    try:
        await set_timetable(name_sheet, user_data, timetable)
    except Exception:
        await create_new_timetable_in_spreadsheets(name_sheet)
        await set_timetable(name_sheet, user_data, timetable)


async def create_new_timetable_in_spreadsheets(name_sheet):
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': name_sheet
                    }
                }
            },]
        }).execute()


async def set_timetable(name_sheet, user_data, timetable: dict):
    row = user_data[f"{QueryField.ID.value}"] + 1
    result = await sql.select(
        database_name,
        table_workers,
        f"{QueryField.USER_ID.value} = ?",
        user_data[f"{QueryField.USER_ID.value}"],
        [f"{WorkerField.FULL_NAME.value}"]
    )
    values = [result[0][0]] + list(timetable.values()) + [await get_number_hours(timetable)]
    print(values)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": {
                "range": f"{name_sheet}!A{row}:I{row}",
                "majorDimension": "ROWS",
                "values": [values,]
            }
        }
    ).execute()


@router.message(
    StateFilter(CoordinationTimetables.rejection),
    IsAdmin()
)
async def take_rejection_reason(message: types.Message, state: FSMContext):
    await message.answer("Причина отказа отправлена...")
    user_data = await state.get_data()
    id_worker = user_data[f"{QueryField.USER_ID.value}"]
    await bot.send_message(id_worker, f"Ваше расписание отклонено по причине: {message.text}")
    await delete_query(message, state)


async def delete_query(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    query_id = user_data[f"{QueryField.ID.value}"]
    # await sql.delete(database_name, table_queries, f"{QueryField.ID.value} = ?", query_id)
    await show_next_timetable(message, state)
