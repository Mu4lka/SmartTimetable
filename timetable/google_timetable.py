import asyncio
import logging
from enum import Enum

import loader
from utils.google import AsyncSpreadsheets, Sheet
from utils.google.enums import Dimension
from utils.google import GridRange
from utils.other import TimeRange
from utils.other.working_with_time import get_week_range, get_datetime_now


def html_color_to_json(html_color):
    if html_color.startswith("#"):
        html_color = html_color[1:]
    return {"red": int(html_color[0:2], 16) / 255.0,
            "green": int(html_color[2:4], 16) / 255.0,
            "blue": int(html_color[4:6], 16) / 255.0}


class Background(dict, Enum):
    MORNING = html_color_to_json("#B6D7A8")
    AFTERNOON = html_color_to_json("#FFE599")
    EVENING = html_color_to_json("#F9CB9C")
    NONE = html_color_to_json("#FFFFFF")


class GoogleTimetable:
    def __init__(self, spreadsheets: AsyncSpreadsheets):
        self.__spreadsheets = spreadsheets
        self.sheets = {}

    @staticmethod
    async def get_element_position(entry_element: list, sheet_name: str):
        timetable = await loader.timetable_storage.get_current_timetable(sheet_name)
        for item in range(len(timetable)):
            try:
                if entry_element[0] == timetable[item][0]:
                    return item + 1
            except Exception:
                pass
        return len(timetable) + 1

    async def write_element(self, element: list, sheet_name: str):
        try:
            position = await self.get_element_position(element, sheet_name)
            await self.__spreadsheets.async_batch_update_values(
                f"{sheet_name}!A{position}:Z{position}",
                Dimension.ROWS,
                [element, ]
            )
            await self.__paint_background(element, position, sheet_name)
        except Exception as e:
            logging.exception(e)
            await self.copy_timetable(sheet_name)
            await self.write_element(element, sheet_name)

    @staticmethod
    def get_week_range_name(day: int = 7):
        next_monday, next_sunday = get_week_range(get_datetime_now().date(), day)
        return f"{next_monday.strftime('%d.%m')}-{next_sunday.strftime('%d.%m')}"

    async def set_sheets(self):
        try:
            spreadsheets = await self.__spreadsheets.async_get_spreadsheets()
            sheets = {}
            for sheet in spreadsheets['sheets']:
                sheet = Sheet(sheet['properties'])
                title = sheet.title
                sheets.update({title: sheet})
            self.sheets = sheets
        except Exception as error:
            print(f"[WARNING] Failed to get sheets from Google sheet [TO_RETRY]!"
                  f"\nDetails: {error}")
            await asyncio.sleep(0.2)
            await self.set_sheets()

    async def copy_timetable(self, new_sheet_name: str):
        await self.set_sheets()
        current_week = self.get_week_range_name(0)
        try:
            sheet_id = self.sheets[current_week].sheetId
        except Exception as error:
            print(f"[WARNING] Not found a sheet to copy with the name {current_week}!\nDetails: {error}")
            first_sheet_id = list(self.sheets.values())[0].sheetId
            sheet_id = first_sheet_id
        try:
            await self.__spreadsheets.async_duplicate_sheet(sheet_id, new_sheet_name)
        except Exception as error:
            print(f"[WARNING] Failed to copy first sheet!\nDetails: {error}")

    @staticmethod
    def __get_background(start_shift: str):
        backgrounds = {
            TimeRange("05:00", "11:59"): Background.MORNING,
            TimeRange("12:00", "15:59"): Background.AFTERNOON,
            TimeRange("16:00", "04:59"): Background.EVENING
        }
        try:
            for time_range, background in backgrounds.items():
                if time_range.time_is_in_range(start_shift):
                    return background
        except Exception as e:
            logging.error(e)
        return Background.NONE

    async def __paint_background(self, element: list, position: int, sheet_name: str):
        values = []
        for item in element:
            start_shift = item.split('-')[0]
            values.append({
                'userEnteredFormat':
                    {'backgroundColor': self.__get_background(start_shift).value}})
        request = {
            'updateCells':
                {'fields': 'userEnteredFormat',
                 'range': GridRange.to_grid_range_json(
                     self.sheets[sheet_name].sheetId,
                     f"A{position}:I{position}"),
                 'rows': [{'values': values}]}}
        await self.__spreadsheets.async_batch_update([request, ])
