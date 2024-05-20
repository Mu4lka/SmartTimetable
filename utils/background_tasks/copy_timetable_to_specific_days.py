import asyncio

from data import settings
from loader import google_timetable
from timetable import GoogleTimetable
from utils.other.working_with_time import get_datetime_now


async def copy_timetable_to_specific_days():
    while True:
        if get_datetime_now().weekday() in settings.CERTAIN_DAYS:
            await asyncio.sleep(1)
            next_week_name = GoogleTimetable.get_week_range_name()
            await google_timetable.copy_timetable(next_week_name)
        await asyncio.sleep(3600)
