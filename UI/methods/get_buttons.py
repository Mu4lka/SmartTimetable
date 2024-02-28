from aiogram import types

from UI.buttons.data_buttons import admin_buttons, worker_buttons
from filters import IsAdmin, IsWorker


async def get_buttons(message: types.Message, user_id: int = None):
    if await IsAdmin().__call__(message, user_id):
        return admin_buttons
    elif await IsWorker().__call__(message, user_id):
        return worker_buttons
    else:
        return
