import asyncio

from utils.google_sheets.base_spreadsheets import BaseSpreadsheets
from utils.google_sheets.enums import Dimension


class Spreadsheets(BaseSpreadsheets):
    async def batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._batch_update_values,
            sheet_range,
            dimension,
            values
        )

    async def get_values(self, sheet_range: str, dimension: Dimension):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._get_values,
            sheet_range,
            dimension
        )

    async def batch_update(self, requests: list):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._batch_update,
            requests
        )
