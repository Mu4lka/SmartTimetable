import asyncio

from google_sheets import spreadsheets
from utils.google.enums import Dimension
from utils.methods.calculate_time_difference import UnitTime
from utils.other import Event


class Timetable:
    def __init__(self):
        self.__data = []
        self.on_update = Event()
        self.on_change = Event()

        self.__running = False

    def get_data(self):
        return self.__data.copy()

    async def start_update(self):
        self.__running = True
        await self.__update()

    def stop_update(self):
        self.__running = False

    @staticmethod
    async def get_current_data():
        result = await spreadsheets.async_get_values("A1:Z1000", Dimension.ROWS)
        return result["values"]

    async def __update(self):
        while self.__running:
            current_data = await self.get_current_data()
            await self.on_update.invoke(self.__data.copy())
            for item in range(len(self.__data)):
                try:
                    if self.__data[item] != current_data[item]:
                        await self.on_change.invoke(current_data[item].copy())
                except Exception as error:
                    print(f"[SAFE][ERROR_200] - {error}")
            self.__data = current_data
            await asyncio.sleep(UnitTime.MINUTES.value)
