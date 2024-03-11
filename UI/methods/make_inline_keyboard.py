from typing import Union

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def make_inline_keyboard(buttons: Union[list, dict]):
    builder = InlineKeyboardBuilder()
    callbacks_data = await get_callbacks_data(buttons)
    index = 0
    for button in buttons:
        builder.row(InlineKeyboardButton(text=str(button), callback_data=str(callbacks_data[index])))
        index = index + 1
    return builder.as_markup()


async def get_callbacks_data(buttons: Union[list, dict]):
    if isinstance(buttons, dict):
        return list(buttons.values())
    else:
        return buttons
