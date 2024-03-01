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
from filters import IsWorker


router = Router()


class SendingTimetableByWorker(StatesGroup):
    begin = State()
    take_timetable = State()


@router.callback_query(
    StateFilter(None),
    IsWorker(),
    F.data == WorkerButton.SEND_MY_TIMETABLE.value
)
async def sending_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Чтобы отправить расписание, нужно его составить",
        reply_markup=await make_inline_keyboard([OtherButton.BEGIN.value]))
    await state.set_state(SendingTimetableByWorker.begin)


@router.callback_query(
    StateFilter(SendingTimetableByWorker.begin),
    IsWorker(),
    F.data == OtherButton.BEGIN.value
)
async def show_template(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(constants.MESSAGE_USING_TEMPLATE)
    await state.set_state(SendingTimetableByWorker.take_timetable)


@router.message(
    StateFilter(SendingTimetableByWorker.take_timetable),
    IsWorker()
)
async def take_template(message: types.Message, state: FSMContext):
    min_number_hours = 40
    min_number_weekend = 2

    try:
        timetable = await get_timetable(message.text.split("\n"))
        number_hours = await get_number_hours(timetable)
        number_weekend = list(timetable.values()).count("вых")
        await check_timetable(timetable, number_hours, min_number_hours, number_weekend, min_number_weekend)
        print(timetable)
        await message.answer(
            f"Количество часов: {number_hours}\nКоличество выходных: {number_weekend}\n\n",
            reply_markup=await make_inline_keyboard(["Отправить расписание", "Изменить"])
        )
        await show_main_menu(message)
        await state.clear()
    except Exception as error:
        await message.answer(str(error))


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


async def get_number_hours(timetable: dict):
    number_hours = 0
    full_dial = {**dial.hours, **dial.half_hours, **dial.hours_first_zero, **dial.half_hours_first_zero}
    for day, shift in list(timetable.items()):
        try:
            number_hours = number_hours + await get_shift_duration(shift, full_dial)
        except Exception:
            raise ValueError(f"Значение смены \"{day}: {shift}\" было введено неверно, попробуйте еще раз...")
    return number_hours


async def get_shift_duration(shift: str, full_dial: dict):
    if shift == "вых":
        return 0.0

    time = shift.split("-", 1)
    time_start, time_end = time
    time_start_value = float(full_dial.get(time_start))
    time_end_value = float(full_dial.get(time_end))
    return (time_start_value >= time_end_value) * constants.DAY_END - (time_start_value - time_end_value)


async def check_timetable(
        timetable: dict,
        number_hours: float,
        min_number_hours: float,
        number_weekend: int,
        min_number_weekend: int
):
    if len(timetable) < 7:
        raise ValueError("Не все заполнены дни, попробуйте ещё раз...")

    if number_hours < min_number_hours:
        raise ValueError(
            f"Количество часов за неделю меньше, чем задано!\n"
            f"Должно не меньше {min_number_hours}. Пришло: {number_hours}. попробуйте ещё раз..."
        )

    if number_weekend > min_number_weekend:
        raise ValueError(
            "Количество выходных в неделю больше, чем задано!\n"
            f"Должно быть не больше {min_number_weekend}. Пришло: {number_weekend}. попробуйте ещё раз..."
        )
