import asyncio

import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from utils.google_sheets.enums import Dimension
from utils.google_sheets.methods import write_batch_update_values, get_values, update_spreadsheets


class Spreadsheets:
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"])
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build("sheets", "v4", http=http_auth)

        self.__spreadsheet_id: str = spreadsheet_id
        self.spreadsheets = service.spreadsheets()

    async def get_values(self, sheet_range: str, dimension: Dimension):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            get_values,
            self.spreadsheets,
            self.__spreadsheet_id,
            sheet_range,
            dimension
        )

    async def write_batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            write_batch_update_values,
            self.spreadsheets,
            self.__spreadsheet_id,
            sheet_range,
            dimension,
            values
        )

    async def update(self, requests: list):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            update_spreadsheets,
            self.spreadsheets,
            self.__spreadsheet_id,
            requests
        )
