from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums import OtherButton
from UI.methods import show_main_menu
from filters import IsWorker


router = Router()


class ShiftChange(StatesGroup):
    start = State()
    take_old_shift = State()
    take_new_shift = State()


@router.callback_query(StateFilter(ShiftChange.start), IsWorker(), F.data == OtherButton.CHANGE_SHIFT.value)
async def change_shift(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("В реализации")
    await show_main_menu(callback_query.message, worker_buttons)
    await state.clear()
