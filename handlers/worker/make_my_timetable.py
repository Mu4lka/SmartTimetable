from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu
from data import constants
from filters import IsWorker


router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.MAKE_MY_TIMETABLE.value)
async def select_weekend(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        f"Команда \"{WorkerButton.MAKE_MY_TIMETABLE.value}\" {constants.NOT_AVAILABLE_YET}"
    )
    await show_main_menu(callback_query.message, worker_buttons)
