from typing import Any

from data.config import SPREADSHEET_ID
from database.database_config import database_name, table_workers
from database.enums import QueryField, WorkerField
from google_sheets import service
from handlers.worker.send_timetable import calculate_number_of_hours
from utils import sql


async def get_number_row(worker_id):
    result: list = await sql.select(
        database_name,
        table_workers,
    )
    index = 0
    for worker in result:
        if worker_id in worker:
            return index
        index += 1


async def write_timetable(sheet_name: str, timetable: dict, user_data: Any):
    worker_id = user_data["query_data"][QueryField.WORKER_ID.value]
    number_row = await get_number_row(worker_id) + 2
    values = (
            [user_data[WorkerField.FULL_NAME.value]]
            + list(timetable.values()) +
            [await calculate_number_of_hours(timetable)]
    )
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": {
                "range": f"{sheet_name}!A{number_row}:I{number_row}",
                "majorDimension": "ROWS",
                "values": [values, ]
            }
        }
    ).execute()
