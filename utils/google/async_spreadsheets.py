import asyncio
from abc import ABC, abstractmethod

from utils.google.enums import Dimension
from utils.google.spreadsheets import Spreadsheets


class BaseAsyncSpreadsheets(ABC):
    @abstractmethod
    async def async_batch_update(self, requests: list):
        pass

    @abstractmethod
    async def async_get_values(self, sheet_range: str, dimension: Dimension):
        pass

    @abstractmethod
    async def async_batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        pass


class AsyncSpreadsheets(BaseAsyncSpreadsheets, Spreadsheets):
    async def async_batch_update_values(self, sheet_range: str, dimension: Dimension, values: list[list]):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.batch_update_values,
            sheet_range,
            dimension,
            values
        )

    async def async_get_values(self, sheet_range: str, dimension: Dimension):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.get_values,
            sheet_range,
            dimension
        )

    async def async_batch_update(self, requests: list):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.batch_update,
            requests
        )
