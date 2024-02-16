from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import worker_buttons
from UI.show_main_menu import show_main_menu
from enums.menu import WorkerButton
from filters.is_worker import IsWorker


router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SELECT_WEEKEND.value)
async def select_weekend(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выбрать выходные")
    await show_main_menu(callback_query.message, worker_buttons)
