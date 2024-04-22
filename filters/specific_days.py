from aiogram import types

from utils.other import Week
from aiogram.filters import Filter
from datetime import datetime


class SpecificDays(Filter):
    def __init__(self, weekdays: list[Week]):
        self.__weekdays = weekdays

    async def __call__(self, callback_query: types.CallbackQuery):
        return Week(datetime.now().weekday()) in self.__weekdays
