import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.buttons import dial
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from database.database_config import database_name, table_workers, table_queries
from database.enums import WorkerField, QueryField
from database.enums.query_field import QueryType
from filters import IsWorker
from utils import sql

router = Router()


class SendingTimetableByWorker(StatesGroup):
    timetable = State()
    apply = State()


@router.callback_query(
    StateFilter(None),
    IsWorker(),
    F.data == WorkerButton.SEND_MY_TIMETABLE.value
)
async def show_template(callback_query: types.CallbackQuery, state: FSMContext):
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.ID_TELEGRAM.value} = ?",
        callback_query.from_user.id,
        [f"{WorkerField.NUMBER_HOURS.value}", f"{WorkerField.NUMBER_WEEKEND.value}"]
    )
    min_number_hours, max_number_weekend = result[0]
    await state.update_data(
        min_number_hours=min_number_hours,
        max_number_weekend=max_number_weekend
    )
    await callback_query.message.edit_text(
        f"{constants.MESSAGE_USING_TEMPLATE}"
        f"Ваше минимальное количество часов на неделю: {min_number_hours}\n"
        f"Ваше максимальное количество выходных: {max_number_weekend}"
    )
    await state.set_state(SendingTimetableByWorker.timetable)


@router.message(
    StateFilter(SendingTimetableByWorker.timetable),
    IsWorker()
)
async def take_template(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    min_number_hours = user_data["min_number_hours"]
    max_number_weekend = user_data["max_number_weekend"]

    try:
        timetable = await get_timetable(message.text.split("\n"))
        number_hours = await get_number_hours(timetable)
        number_weekend = list(timetable.values()).count("вых")
        await check_timetable(timetable, number_hours, min_number_hours, number_weekend, max_number_weekend)
        await message.answer(
            f"Количество часов: {number_hours}\nКоличество выходных: {number_weekend}\n\n",
            reply_markup=await make_inline_keyboard(
                [OtherButton.SEND_TIMETABLE.value, OtherButton.CHANGE.value]
            )
        )
        await state.update_data(timetable=await sort_timetable(timetable))
        await state.set_state(SendingTimetableByWorker.apply)
    except Exception as error:
        await message.answer(str(error))


@router.callback_query(
    StateFilter(SendingTimetableByWorker.apply),
    IsWorker()
)
async def insert_timetable_in_database(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == OtherButton.CHANGE.value:
        await show_template(callback_query, state)
    elif callback_query.data == OtherButton.SEND_TIMETABLE.value:
        user_data = await state.get_data()
        query = {
            f"{QueryField.ID_TELEGRAM.value}": callback_query.from_user.id,
            f"{QueryField.TYPE.value}": QueryType.SENDING_TIMETABLE_BY_WORKER.value,
            f"{QueryField.QUERY_TEXT.value}": json.dumps(user_data["timetable"]),
        }
        await sql.insert(database_name, table_queries, query)
        await callback_query.message.edit_text("Вы отправили расписание!\nОжидайте подтверждение руководителя...")
        await show_main_menu(callback_query.message, user_id=callback_query.from_user.id)
        await state.clear()


async def get_timetable(lines: list):
    week = constants.week_abbreviated.copy()
    timetable = {}
    for line in lines:
        shift = line.lower().replace(' ', '').split(":", 1)
        try:
            day = week.pop(week.index(shift[0]))
        except Exception:
            raise ValueError(constants.INVALID_INPUT)
        timetable.update({day: shift[1]})
    return timetable


async def sort_timetable(timetable: dict):
    sorted_timetable = {day: None for day in constants.week_abbreviated}
    sorted_timetable.update(timetable)
    return sorted_timetable


async def get_number_hours(timetable: dict):
    number_hours = 0
    for day, shift in list(timetable.items()):
        try:
            number_hours = number_hours + await get_shift_duration(shift)
        except Exception:
            raise ValueError(f"Значение смены \"{day}: {shift}\" было введено неверно, попробуйте еще раз...")
    return number_hours


async def get_shift_duration(shift: str):
    if shift == "вых":
        return 0.0

    time_start, time_end = shift.split("-", 1)
    time_start_value = float(dial.full_dial.get(time_start))
    time_end_value = float(dial.full_dial.get(time_end))
    return (time_start_value >= time_end_value) * constants.DAY_END - (time_start_value - time_end_value)


async def check_timetable(
        timetable: dict,
        number_hours: float,
        min_number_hours: float,
        number_weekend: int,
        max_number_weekend: int
):
    if not len(timetable) == len(constants.week_abbreviated):
        raise ValueError("Не все заполнены дни, попробуйте ещё раз...")

    if number_hours < min_number_hours:
        raise ValueError(
            f"Количество часов за неделю меньше, чем задано!\n"
            f"Должно не меньше {min_number_hours}. Всего: {number_hours}. попробуйте ещё раз..."
        )

    if number_weekend > max_number_weekend:
        raise ValueError(
            "Количество выходных в неделю больше, чем задано!\n"
            f"Должно быть не больше {max_number_weekend}. Всего: {number_weekend}. попробуйте ещё раз..."
        )
