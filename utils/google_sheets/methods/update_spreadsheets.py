from typing import Any


def update_spreadsheets(
        spreadsheets: Any,
        spreadsheet_id: str,
        requests: list):
    spreadsheets.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}).execute()
