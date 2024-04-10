import asyncio

from google_sheets import spreadsheets
from utils.google_sheets.enums import Dimension
from utils.other import Event


class Timetable:
    def __init__(self):
        self.sheet_timetable = []
        self.on_update = Event()
        self.on_change = Event()

        self.__running = False

    async def start_update(self):
        self.__running = True
        await self.__update()

    def stop_update(self):
        self.__running = False

    async def __get_sheet_timetable(self) -> list:
        result = await spreadsheets.get_values("A1:Z1000", Dimension.ROWS)
        return result["values"]

    async def __update(self):
        while self.__running:
            current_sheet_timetable = await self.__get_sheet_timetable()
            await self.on_update.invoke(self.sheet_timetable.copy())
            for item in range(len(self.sheet_timetable)):
                try:
                    if self.sheet_timetable[item] != current_sheet_timetable[item]:
                        await self.on_change.invoke(current_sheet_timetable[item])
                except Exception:
                    pass
            self.sheet_timetable = current_sheet_timetable
            await asyncio.sleep(60)
