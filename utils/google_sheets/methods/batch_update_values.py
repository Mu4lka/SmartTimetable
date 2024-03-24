from typing import Any

from utils.google_sheets.enums import Dimension


def batch_update_values(
        spreadsheets: Any,
        spreadsheet_id: str,
        sheet_range: str,
        dimension: Dimension,
        values: list[list]):
    spreadsheets.values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": {
                "range": sheet_range,
                "majorDimension": dimension.value,
                "values": values
            }
        }
    ).execute()
