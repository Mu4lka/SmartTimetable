from typing import Any

from utils.google_sheets.enums import Dimension


def write_batch_update_values(
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
