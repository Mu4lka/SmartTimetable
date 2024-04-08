import logging

from aiogram import Router

from aiogram.types import ErrorEvent

from data import constants
from loader import bot

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    file_name = "errors.txt"
    with open(file_name, "a") as file:
        error = "ЕRROR"
        text = (
            f"{error:-^80}\n"
            f"update: {str(event.update)}\n\n"
            f"ErrorText: {str(event.exception)}\n\n\n")
        file.write(text)
        await bot.send_message(constants.CREATOR_ID, f"ErrorText: {str(event.exception)}")
        logging.exception(text)
