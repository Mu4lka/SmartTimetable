import asyncio
from datetime import datetime

from filters.specific_days import Week
from handlers.worker.send_timetable import certain_days
from loader import timetable
from utils.methods.calculate_time_difference import UnitTime
from utils.methods.get_next_week_range import get_sheet_name


async def copy_sheet_for_next_week():
    while True:
        if Week(datetime.now().weekday()) in certain_days:
            new_name = get_sheet_name()
            try:
                await asyncio.sleep(UnitTime.SECONDS.value)
                try:
                    current_name = get_sheet_name(0)
                    await timetable.copy_sheet(new_name, current_name)
                except Exception as error:
                    print(f"[WARNING] Failed to copy sheet by name. The first sheet will be copied!\nDetails: {error}")
                    await timetable.copy_sheet(new_name)
            except Exception as error:
                print(f"[WARNING] Failed to copy sheet!\nDetails: {error}")
        await asyncio.sleep(UnitTime.HOURS.value)
