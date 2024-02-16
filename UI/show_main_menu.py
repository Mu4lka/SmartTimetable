from aiogram import types

from UI.get_buttons import get_buttons
from UI.make_inline_keyboard import make_inline_keyboard
from data import constants


async def show_main_menu(message: types.Message, buttons: list = None, user_id: int = None):
    if buttons is None:
        buttons = await get_buttons(message, user_id)
    await message.answer(
        f"{constants.SELECT_COMMAND}",
        reply_markup=await make_inline_keyboard(buttons)
    )
