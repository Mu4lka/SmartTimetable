import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from UI.buttons.data_buttons import admin_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import show_main_menu, make_inline_keyboard
from database import WorkerField, QueryField, QueryType
from filters import IsAdmin, IsPrivate
from loader import bot, query_table, worker_table, google_timetable
from timetable import GoogleTimetable
from utils.methods import make_form
from utils.services.notification_system.notify_admins.notify_not_accepted_timetables import \
    accepted_full_names


class CoordinationTimetables(StatesGroup):
    coordination = State()
    rejection = State()


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.COORDINATE_TIMETABLES.value)
async def coordinate_timetables(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    queries = await query_table.get_queries(QueryType.SENDING_TIMETABLE)

    if await has_pending_queries(queries, callback_query.message, state):
        await state.update_data(queries=queries)
        await show_next_timetable(callback_query.message, state)
        await state.set_state(CoordinationTimetables.coordination)


@router.message(StateFilter(CoordinationTimetables.coordination), IsAdmin())
async def show_next_timetable(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    queries = user_data["queries"]
    if await has_pending_queries(queries, message, state):
        query_data = await extract_query_data(queries)
        worker_data = await worker_table.select(
            f"{WorkerField.ID.value} = ?",
            (query_data[QueryField.WORKER_ID.value],),
            [WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
        )
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


@router.callback_query(
    StateFilter(CoordinationTimetables.coordination),
    IsAdmin(),
    F.data == OtherButton.ACCEPT.value
)
async def accept_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    query = json.loads(user_data["query_data"][QueryField.QUERY_TEXT.value])
    accepted_full_names.add(user_data[WorkerField.FULL_NAME.value])
    _timetable = query["timetable"]
    await write_item_in_timetable(user_data, _timetable)
    await callback_query.message.edit_text("Вы приняли расписание...")
    await bot.send_message(user_data[WorkerField.TELEGRAM_ID.value], f"Ваше расписание принято!")
    await delete_query(callback_query.message, state)


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


async def make_form_for_coordination_timetable(_timetable: dict, full_name: str):
    form = make_form(_timetable["timetable"])
    return f"Расписание сотрудника {full_name}:\n\n<pre>{form}</pre>\nКоличество часов: {_timetable['hours_number']}"


async def write_item_in_timetable(user_data, timetable_element: dict):
    worker_id = user_data["query_data"][QueryField.WORKER_ID.value]
    position = await worker_table.worker_number(worker_id) + 2
    element = ([user_data[WorkerField.FULL_NAME.value]]
               + list(timetable_element.values()))
    next_week_name = GoogleTimetable.get_week_range_name()
    await google_timetable.write_element(element, position, next_week_name)


async def delete_query(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    query_id = user_data["query_data"][QueryField.ID.value]
    await query_table.delete(
        f"{QueryField.ID.value} = ?",
        (query_id,))
    await show_next_timetable(message, state)
