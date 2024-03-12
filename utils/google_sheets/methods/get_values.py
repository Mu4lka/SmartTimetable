from typing import Any

from utils.google_sheets.enums import Dimension


def get_values(
        spreadsheets: Any,
        spreadsheet_id: str,
        sheet_range: str,
        dimension: Dimension):
    return spreadsheets.values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        majorDimension=dimension.value
    ).execute()
