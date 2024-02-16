from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import admin_buttons
from UI.show_main_menu import show_main_menu
from enums.menu import AdminButton
from filters.is_admin import IsAdmin


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.SHOW_WORKERS.value)
async def show_workers(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.from_user.id)
    await callback_query.message.answer("Показываются сотрудники")
    await show_main_menu(callback_query.message, admin_buttons)
