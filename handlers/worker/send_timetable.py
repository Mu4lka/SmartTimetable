import json

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.buttons import dial
from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from database.database_config import database_name, table_workers, table_queries
from database.enums import WorkerField, QueryField
from database.enums.query_field import QueryType
from database.methods import found_from_database, get_worker_parameter_by_telegram_id
from filters import IsWorker
from utils import sql

router = Router()


class SendingTimetable(StatesGroup):
    timetable = State()
    apply = State()


async def get_data_for_sending_timetable(user_id: int):
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.TELEGRAM_ID.value} = ?",
        (user_id,),
        [
            WorkerField.ID.value,
            WorkerField.NUMBER_HOURS.value,
            WorkerField.NUMBER_WEEKEND.value
        ]
    )
    return result[0]


async def send_template(callback_query: types.CallbackQuery, number_hours: int, number_weekend: int):
    await callback_query.message.edit_text(
        f"{constants.EXAMPLE_TEMPLATE}"
        f"Ваше количество часов на неделю: {number_hours}\n"
        f"Ваше количество выходных: {number_weekend}"
    )


async def prepare_template(callback_query: types.CallbackQuery, state: FSMContext):
    worker_id, number_hours, number_weekend = \
        await get_data_for_sending_timetable(callback_query.from_user.id)
    await state.update_data({
        WorkerField.ID.value: worker_id,
        WorkerField.NUMBER_HOURS.value: number_hours,
        WorkerField.NUMBER_WEEKEND.value: number_weekend
    })
    await send_template(callback_query, number_hours, number_weekend)
    await state.set_state(SendingTimetable.timetable)


@router.callback_query(
    StateFilter(None),
    IsWorker(),
    F.data == WorkerButton.SEND_MY_TIMETABLE.value
)
async def start_sending_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    worker_id = await get_worker_parameter_by_telegram_id(
        callback_query.from_user.id,
        WorkerField.ID.value
    )
    if await found_from_database(
            table_queries,
            f"{QueryField.WORKER_ID.value} = ? AND {QueryField.TYPE.value} = ?",
            (worker_id, QueryType.SENDING_TIMETABLE)):
        await callback_query.message.edit_text(constants.INVALID_ABOUT_MORE_THAN_ONE_SCHEDULE)
        await show_main_menu(callback_query.message, worker_buttons)
        return
    else:
        await prepare_template(callback_query, state)


async def make_timetable(lines: list):
    week = constants.week_abbreviated.copy()
    timetable = {}
    for line in lines:
        shift = line.lower().replace(' ', '').split(":", 1)
        try:
            day = week.pop(week.index(shift[0]))
        except Exception:
            raise ValueError(constants.INVALID_TIMETABLE)
        timetable.update({day: shift[1]})
    return timetable


async def calculate_shift_duration(shift: str):
    if shift == constants.day_off:
        return 0.0

    time_start_str, time_end_str = shift.split("-", 1)
    time_start = float(dial.full_dial.get(time_start_str))
    time_end = float(dial.full_dial.get(time_end_str))
    return (time_start >= time_end) * constants.DAY_END - (time_start - time_end)


async def calculate_number_of_hours(timetable: dict):
    number_hours = 0
    for day, shift in list(timetable.items()):
        try:
            number_hours = number_hours + await calculate_shift_duration(shift)
        except Exception:
            raise ValueError(f"Значение смены \"{day}: {shift}\" было введено неверно, попробуйте еще раз...")
    return number_hours


async def check_filled_days(timetable: dict):
    if len(timetable) != len(constants.week_abbreviated):
        raise ValueError("Не все заполнены дни, попробуйте ещё раз...")


async def check_hours_number(number_hours: float, min_number_hours: float):
    if number_hours < min_number_hours:
        raise ValueError(
            f"Количество часов за неделю меньше, чем задано!\n"
            f"Должно быть не менее {min_number_hours}. Всего: {number_hours}. Попробуйте ещё раз..."
        )


async def check_weekend_number(number_weekend: int, max_number_weekend: int):
    if number_weekend > max_number_weekend:
        raise ValueError(
            f"Количество выходных в неделю больше, чем задано!\n"
            f"Должно быть не более {max_number_weekend}. Всего: {number_weekend}. Попробуйте ещё раз..."
        )


async def check_timetable(
        timetable: dict,
        number_hours: float,
        number_weekend: int,
        user_data: dict
):
    await check_filled_days(timetable)
    await check_hours_number(number_hours, user_data[WorkerField.NUMBER_HOURS.value])
    await check_weekend_number(number_weekend, user_data[WorkerField.NUMBER_WEEKEND.value])


async def sort_timetable(timetable: dict):
    sorted_timetable = {day: None for day in constants.week_abbreviated}
    sorted_timetable.update(timetable)
    return sorted_timetable


@router.message(
    StateFilter(SendingTimetable.timetable),
    IsWorker()
)
async def process_timetable_input(message: types.Message, state: FSMContext):
    try:
        timetable = await make_timetable(message.text.split("\n"))
        number_hours = await calculate_number_of_hours(timetable)
        number_weekend = list(timetable.values()).count(constants.day_off)
        await check_timetable(timetable, number_hours, number_weekend, await state.get_data())
        await message.answer(
            f"Количество часов: {number_hours}\nКоличество выходных: {number_weekend}\n\n",
            reply_markup=await make_inline_keyboard(
                [OtherButton.SEND_TIMETABLE.value, OtherButton.CHANGE.value]
            )
        )
        await state.update_data(timetable=await sort_timetable(timetable))
        await state.set_state(SendingTimetable.apply)
    except Exception as error:
        await message.answer(str(error))


async def make_query(worker_id: int, query_type: QueryType, query: dict):
    return {
        QueryField.WORKER_ID.value: worker_id,
        QueryField.TYPE.value: query_type.value,
        QueryField.QUERY_TEXT.value: json.dumps(query),
    }


async def insert_query_in_database(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await sql.insert(
        database_name,
        table_queries,
        await make_query(
            user_data[WorkerField.ID.value],
            QueryType.SENDING_TIMETABLE,
            user_data["timetable"]
        )
    )
    await callback_query.message.edit_text(
        "Вы отправили расписание!\nОжидайте подтверждение руководителя..."
    )
    await show_main_menu(callback_query.message, worker_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(SendingTimetable.apply),
    IsWorker()
)
async def handle_input(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == OtherButton.CHANGE.value:
        await prepare_template(callback_query, state)
    elif callback_query.data == OtherButton.SEND_TIMETABLE.value:
        await insert_query_in_database(callback_query, state)
