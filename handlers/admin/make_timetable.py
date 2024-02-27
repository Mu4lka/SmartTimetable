from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import admin_buttons
from UI.show_main_menu import show_main_menu
from data import constants
from enums.main_menu import AdminButton
from filters.is_admin import IsAdmin


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.MAKE_TIMETABLE.value)
async def generate_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        f"Команда \"{AdminButton.MAKE_TIMETABLE.value}\" {constants.NOT_AVAILABLE_YET}"
    )
    await show_main_menu(callback_query.message, admin_buttons)
