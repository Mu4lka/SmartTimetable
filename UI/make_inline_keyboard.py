from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def make_inline_keyboard(buttons: list[str], indexed: bool = False):
    builder = InlineKeyboardBuilder()
    if indexed:
        for item in range(len(buttons)):
            builder.row(InlineKeyboardButton(text=buttons[item], callback_data=str(item)))
    else:
        for button in buttons:
            builder.row(InlineKeyboardButton(text=button, callback_data=button))
    return builder.as_markup()
