from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import worker_buttons
from UI.show_main_menu import show_main_menu
from enums.menu import WorkerButton
from filters.is_worker import IsWorker


router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.CHANGE_SHIFT.value)
async def change_shift(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Изменяется смена")
    await show_main_menu(callback_query.message, worker_buttons)
