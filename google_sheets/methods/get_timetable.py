from google_sheets.loader import spreadsheets
from utils.google_sheets.enums import Dimension


async def get_timetable(dimension: Dimension):
    result = await spreadsheets.get_values("A1:I1000", dimension)
    return result["values"]
