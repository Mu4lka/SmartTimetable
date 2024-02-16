from aiogram import types
from aiogram.filters import Filter

from filters.is_admin import IsAdmin
from filters.is_worker import IsWorker


class IsAuthorized(Filter):
    async def __call__(self, message: types.Message):
        return await IsAdmin().__call__(message) or await IsWorker().__call__(message)
