import logging
from pprint import pprint

from aiogram import Router

from aiogram.types import ErrorEvent


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
        logging.exception(text)
