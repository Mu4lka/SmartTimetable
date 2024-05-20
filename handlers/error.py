import logging

from aiogram import Router

from aiogram.types import ErrorEvent

from database import ErrorField
from loader import error_table
from utils.other.working_with_time import get_datetime_now

router = Router()


@router.error()
async def handle_error(event: ErrorEvent):
    await error_table.insert({
        ErrorField.TIME.value: get_datetime_now(),
        ErrorField.TEXT.value: str(event.exception),
        ErrorField.JSON.value: str(event),
    })
    logging.exception(event.exception)
