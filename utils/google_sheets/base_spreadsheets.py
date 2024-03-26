from abc import ABC, abstractmethod

import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from utils.google_sheets.enums import Dimension


class BaseSpreadsheets(ABC):
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"])
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build("sheets", "v4", http=http_auth)

        self.__spreadsheet_id: str = spreadsheet_id
        self.spreadsheets = service.spreadsheets()

    def _batch_update(self, requests: list):
        self.spreadsheets.batchUpdate(
            spreadsheetId=self.__spreadsheet_id,
            body={"requests": requests}
        ).execute()

    def _get_values(self, sheet_range: str, dimension: Dimension):
        return self.spreadsheets.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=sheet_range,
            majorDimension=dimension.value
        ).execute()

    def _batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        self.spreadsheets.values().batchUpdate(
            spreadsheetId=self.__spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": {
                    "range": sheet_range,
                    "majorDimension": dimension.value,
                    "values": values
                }
            }
        ).execute()

    @abstractmethod
    async def batch_update(self, requests: list):
        pass

    @abstractmethod
    async def get_values(self, sheet_range: str, dimension: Dimension):
        pass

    @abstractmethod
    async def batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        pass
