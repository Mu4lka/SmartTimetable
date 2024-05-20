from aiogram import types

from aiogram.filters import Filter

from utils.other.working_with_time import get_datetime_now


class SpecificDays(Filter):
    def __init__(self, weekdays: list[int]):
        self.__weekdays = weekdays

    async def __call__(self, callback_query: types.CallbackQuery):
        return get_datetime_now().weekday() in self.__weekdays
