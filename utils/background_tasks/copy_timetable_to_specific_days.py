import asyncio

from data import settings
from utils.methods.get_datetime_now import get_datetime_now
from loader import google_timetable
from timetable import GoogleTimetable


async def copy_timetable_to_specific_days():
    while True:
        if get_datetime_now().weekday() in settings.CERTAIN_DAYS:
            await asyncio.sleep(1)
            next_week_name = GoogleTimetable.get_week_range_name()
            await google_timetable.copy_timetable(next_week_name)
        await asyncio.sleep(3600)
