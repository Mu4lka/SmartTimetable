from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.data_buttons import worker_buttons
from UI.make_inline_keyboard import make_inline_keyboard
from UI.show_main_menu import show_main_menu
from data import constants
from data.config import SPREADSHEET_ID
from database.database_config import database_name, table_workers
from enums.database_field import DatabaseField
from enums.main_menu import WorkerButton
from enums.other_button import OtherButton
from filters.is_worker import IsWorker
import google_sheets
from handlers.worker.change_shift import ShiftChange
from utils import sql

router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SHOW_MY_TIMETABLE.value)
async def show_my_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    name = await get_name(callback_query.from_user.id)
    timetable = await get_timetable_from_google_sheets()
    row = await find_row_by_name_from_timetable(timetable, name)
    if row is None:
        await callback_query.message.edit_text(
            f"К сожалению Вас, {name}, в расписании не нашел, обратитесь к РОПу"
        )
        await show_main_menu(callback_query.message, worker_buttons)
        return

    shifts = await make_shifts(row)
    await callback_query.message.edit_text(
        await get_text_about_your_timetable(shifts),
        reply_markup=await make_inline_keyboard([OtherButton.CHANGE_SHIFT.value])
    )
    await state.update_data(timetable=timetable, shifts=shifts)
    await state.set_state(ShiftChange.start)


async def get_name(user_id: int):
    result = await sql.select(
        database_name,
        table_workers,
        f"{DatabaseField.ID_TELEGRAM.value} = ?",
        user_id,
        [DatabaseField.FULL_NAME.value]
    )
    return result[0][0]


async def get_timetable_from_google_sheets():
    result = google_sheets.service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1:O100',
        majorDimension='ROWS'
    ).execute()
    return result.get("values")


async def find_row_by_name_from_timetable(timetable: list, name: str):
    for row in timetable:
        if name in row:
            return row
    return


async def get_text_about_your_timetable(shifts: list):
    text = ""
    for day_week, shift in list(zip(constants.week_abbreviated, shifts)):
        text = text + f"{day_week}: {shift}\n"
    return text


async def make_shifts(row: list):
    shifts = []
    for index in range(1, len(row), 2):
        first = row[index]
        shift = first
        if index + 1 == len(row):
            shifts.append(shift)
            break
        second = row[index + 1]

        if not second == "":
            if first == "":
                shift = shift + f"{second}"
            else:
                shift = shift + f" и {second}"
        shifts.append(shift)
    return shifts
