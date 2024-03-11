from data import constants
from data.config import SPREADSHEET_ID
from google_sheets import service


async def create_new_timetable(name_sheet):
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": name_sheet
                    }
                }
            },]
        }).execute()
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": {
                "range": f"{name_sheet}!A1:I1",
                "majorDimension": "ROWS",
                "values": [constants.format_timetable, ]
            }
        }
    ).execute()
