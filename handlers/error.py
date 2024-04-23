from datetime import datetime

from aiogram import Router

from aiogram.types import ErrorEvent

from database import ErrorField
from loader import error_table

router = Router()


@router.error()
async def handle_error(event: ErrorEvent):
    await error_table.insert({
        ErrorField.TIME.value: datetime.now(),
        ErrorField.TEXT.value: str(event.exception),
        ErrorField.JSON.value: str(event),
    })
    print(f"\033[31m[ERROR] Telegram error!\nDetails: {event}\033[0m")
