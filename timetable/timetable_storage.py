import asyncio

from utils.google import AsyncSpreadsheets
from utils.google.enums import Dimension
from utils.methods.calculate_time_difference import UnitTime
from utils.other import Event


class TimetableStorage:
    def __init__(self, spreadsheet: AsyncSpreadsheets):
        self.on_update = Event()
        self.on_change = Event()

        self.__spreadsheet = spreadsheet
        self.__data = []
        self.__running = False

    def get_data(self):
        return self.__data.copy()

    async def start_update(self):
        self.__running = True
        await self.__update()

    def stop_update(self):
        self.__running = False

    async def get_current_data(self, sheet_name: str = None):
        sheet_range = "A1:Z1000"
        if isinstance(sheet_name, str):
            sheet_range = sheet_name + "!" + sheet_range
        result = await self.__spreadsheet.async_get_values(
            sheet_range, Dimension.ROWS)
        return result["values"]

    async def __update(self):
        while self.__running:
            try:
                current_data = await self.get_current_data()
            except Exception as error:
                await asyncio.sleep(UnitTime.SECONDS.value)
                print(f"[WARNING] Failed to get data from Google sheet [TO_RETRY]!\nDetails: {error}")
                continue
            await self.on_update.invoke(self.__data.copy())
            for item in range(len(self.__data)):
                try:
                    if self.__data[item] != current_data[item]:
                        await self.on_change.invoke(current_data[item].copy())
                except Exception as error:
                    print(f"[WARNING] Failed to compare timetable\nDetails: {error}")
            self.__data = current_data
            await asyncio.sleep(UnitTime.MINUTES.value)
