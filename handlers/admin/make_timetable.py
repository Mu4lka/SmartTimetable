from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.buttons.data_buttons import admin_buttons
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import show_main_menu
from data import constants
from filters import IsAdmin


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.MAKE_TIMETABLE.value)
async def generate_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        f"Команда \"{AdminButton.MAKE_TIMETABLE.value}\" {constants.NOT_AVAILABLE_YET}"
    )
    await show_main_menu(callback_query.message, admin_buttons)
