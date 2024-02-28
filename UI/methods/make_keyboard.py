from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def make_keyboard(items: list[str]):
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.row(KeyboardButton(text=item))
    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup
