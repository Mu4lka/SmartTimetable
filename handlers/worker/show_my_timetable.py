from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import worker_buttons
from UI.show_main_menu import show_main_menu
from enums.menu import WorkerButton
from filters.is_worker import IsWorker


router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SHOW_MY_TIMETABLE.value)
async def show_my_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Показать мое расписание")
    await show_main_menu(callback_query.message, worker_buttons)
