from enum import Enum

from aiogram import types
from aiogram.filters import Filter
from datetime import datetime


class Week(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class SpecificDays(Filter):
    def __init__(self, weekdays: set[Week]):
        self.__weekdays = weekdays

    async def __call__(self, callback_query: types.CallbackQuery):
        return Week(datetime.now().weekday()) in self.__weekdays
