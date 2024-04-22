import asyncio
from datetime import datetime

from filters.specific_days import Week
from handlers.worker.send_timetable import certain_days
from loader import google_timetable
from timetable import GoogleTimetable
from utils.methods.calculate_time_difference import UnitTime


async def copy_timetable_to_specific_days():
    while True:
        if Week(datetime.now().weekday()) in certain_days:
            await asyncio.sleep(UnitTime.SECONDS.value)
            next_week_name = GoogleTimetable.get_week_range_name()
            await google_timetable.copy_timetable(next_week_name)
        await asyncio.sleep(UnitTime.HOURS.value)