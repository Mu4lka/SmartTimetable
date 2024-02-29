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


class MakingTimetableByWorker(StatesGroup):
    begin = State()
    shift_start = State()
    shift_end = State()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.MAKE_MY_TIMETABLE.value)
async def start_making_my_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Составление расписания",
        reply_markup=await make_inline_keyboard([OtherButton.BEGIN.value]))
    await state.set_state(MakingTimetableByWorker.begin)


@router.callback_query(
    StateFilter(MakingTimetableByWorker.begin),
    IsWorker(),
    F.data == OtherButton.BEGIN.value
)
async def show_dial(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Выберите начало смены...",
        reply_markup=await make_inline_keyboard(list(dial.hour.keys()))
    )
    await state.set_state(MakingTimetableByWorker.shift_start)


@router.callback_query(
    StateFilter(MakingTimetableByWorker.shift_start),
    IsWorker(),
)
async def take_shift_start(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data({"shift_start": callback_query.data})
    await callback_query.message.edit_text(
        f"Начало смены в {callback_query.data}. Теперь выберите конец смены...",
        reply_markup=await make_inline_keyboard(list(dial.hour.keys()))
    )
    await state.set_state(MakingTimetableByWorker.shift_end)


@router.callback_query(
    StateFilter(MakingTimetableByWorker.shift_end),
    IsWorker(),
)
async def take_shift_end(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data({"shift_end": callback_query.data})
    user_data = await state.get_data()
    shift_start = user_data['shift_start']
    shift_end = user_data['shift_end']
    shift_start_value = float(dial.hour.get(shift_start))
    shift_end_value = float(dial.hour.get(shift_end))
    shift_duration = (bool(shift_start_value >= shift_end_value) *
                      constants.DAY_END - (shift_start_value - shift_end_value))
    await callback_query.message.edit_text(
        f"Ваша смена с {shift_start} до {shift_end}."
        f"\nПродолжительность: {shift_duration}"
        f"\nПодтвердить?"
    )
