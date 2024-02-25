from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.data_buttons import worker_buttons
from UI.show_main_menu import show_main_menu
from enums.other_button import OtherButton
from filters.is_worker import IsWorker

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
