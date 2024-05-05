import asyncio

import loader
from utils.google import AsyncSpreadsheets
from utils.google.enums import Dimension
from utils.methods.calculate_time_difference import UnitTime
from utils.other import Event


class TimetableStorage:
    def __init__(self, spreadsheets: AsyncSpreadsheets):
        self.on_update = Event()
        self.on_change = Event()

        self.__spreadsheets = spreadsheets
        self.__timetable = []
        self.__timetable_name = ""

    def get_timetable(self):
        return self.__timetable.copy()

    async def start_update(self):
        await self.__update()

    async def get_current_timetable(self, sheet_name: str = None):
        sheet_range = "A1:H1000"
        if isinstance(sheet_name, str):
            sheet_range = sheet_name + "!" + sheet_range
        result = await self.__spreadsheets.async_get_values(
            sheet_range, Dimension.ROWS)
        return result["values"]

    async def __update(self):
        while True:
            sheet_name = loader.google_timetable.get_week_range_name(0)
            try:
                current_timetable = await self.get_current_timetable(sheet_name)
            except Exception as error:
                await asyncio.sleep(UnitTime.SECONDS.value)
                print(f"[WARNING] Failed to get data from Google sheet. "
                      f"Try to create a copy of the sheet![TO_RETRY]\nDetails: {error}")
                await loader.google_timetable.copy_timetable(sheet_name)
                continue
            await self.on_update.invoke(self.__timetable.copy())
            if self.__timetable_name == sheet_name:
                for i in range(len(self.__timetable)):
                    try:
                        if self.__timetable[i] != current_timetable[i]:
                            await self.on_change.invoke(
                                current_timetable[i].copy(),
                                self.__timetable[i].copy(),
                                sheet_name
                            )
                    except Exception as error:
                        print(f"[WARNING] The operation failed"
                              f" when comparing timetable elements.\n"
                              f"Details: {error}")
            self.__timetable_name = sheet_name
            self.__timetable = current_timetable
            await asyncio.sleep(UnitTime.MINUTES.value)
