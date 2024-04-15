import asyncio
from datetime import datetime

from filters.specific_days import Week
from google_sheets import spreadsheets
from handlers.worker.send_timetable import certain_days
from timetable import Timetable
from utils.google.enums import Dimension
from utils.methods.calculate_time_difference import UnitTime
from utils.methods.get_next_week_range import get_name_for_sheet_on_next_week


async def copy_sheet_for_next_week():
    while True:
        if Week(datetime.now().weekday()) in certain_days:
            await copy_sheet()
        await asyncio.sleep(UnitTime.HOURS.value)


async def copy_sheet():
    try:
        name = get_name_for_sheet_on_next_week()
        await spreadsheets.async_batch_update([{
            "addSheet": {
                "properties": {
                    "title": name
                }
            }
        }, ])

        await spreadsheets.async_batch_update_values(
            f"{name}!A1:Z1000",
            Dimension.ROWS,
            await Timetable.get_current_data()
        )
    except Exception as error:
        print(f"[SAFE][ERROR_100] - {error}")
