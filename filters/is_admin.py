from aiogram import types
from aiogram.filters import Filter

from data import config


class IsAdmin(Filter):
    async def __call__(self, message: types.Message, user_id: int = None):
        if user_id is None:
            user_id = message.from_user.id

        for admin_id in config.ADMIN_IDS:
            if user_id == admin_id:
                return True
        return False
