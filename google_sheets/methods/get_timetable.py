from google_sheets.loader import spreadsheets
from utils.google_sheets.enums import Dimension


async def get_timetable():
    result = await spreadsheets.get_values("A1:I100", Dimension.ROWS)
    return result["values"]
