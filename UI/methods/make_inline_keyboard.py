from typing import Union

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def make_inline_keyboard(buttons: Union[list[str], dict[str, str]]):
    builder = InlineKeyboardBuilder()
    callbacks_data = await get_callbacks_data(buttons)
    index = 0
    for button in buttons:
        builder.row(InlineKeyboardButton(text=button, callback_data=callbacks_data[index]))
        index = index + 1
    return builder.as_markup()


async def get_callbacks_data(buttons: Union[list[str], dict[str, str]]):
    if isinstance(buttons, dict):
        return list(buttons.values())
    else:
        return buttons
