from aiogram import types

from utils.methods.get_datetime_now import get_datetime_now
from aiogram.filters import Filter


class SpecificDays(Filter):
    def __init__(self, weekdays: list[int]):
        self.__weekdays = weekdays

    async def __call__(self, callback_query: types.CallbackQuery):
        return get_datetime_now().weekday() in self.__weekdays
