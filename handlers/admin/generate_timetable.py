from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import admin_buttons
from UI.show_main_menu import show_main_menu
from enums.menu import AdminButton
from filters.is_admin import IsAdmin


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.GENERATE_TIMETABLE.value)
async def generate_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Генерируется расписание")
    await show_main_menu(callback_query.message, admin_buttons)
