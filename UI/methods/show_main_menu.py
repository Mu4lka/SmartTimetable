from aiogram import types

from UI.methods import get_buttons, make_inline_keyboard
from data import constants


async def show_main_menu(message: types.Message, buttons: list = None, user_id: int = None):
    if buttons is None:
        buttons = await get_buttons(message, user_id)
    await message.answer(
        f"{constants.MAIN_MENU}",
        reply_markup=await make_inline_keyboard(buttons)
    )
