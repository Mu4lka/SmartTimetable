from data import constants
from google_sheets import spreadsheets
from utils.google.enums import Dimension


async def create_new_timetable(name_sheet):
    await spreadsheets.async_batch_update([{
        "addSheet": {
            "properties": {
                "title": name_sheet
            }
        }
    },])
    await spreadsheets.async_batch_update_values(
        f"{name_sheet}!A1:I1",
        Dimension.ROWS,
        [constants.format_timetable,]
    )
