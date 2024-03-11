from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import google_sheets
from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from data.config import SPREADSHEET_ID
from database.enums import WorkerField
from database.methods import get_worker_parameter_by_telegram_id
from filters import IsWorker
from handlers.worker.change_shift import ShiftChange
from utils import make_form

router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SHOW_MY_TIMETABLE.value)
async def show_worker_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    full_name = await get_worker_parameter_by_telegram_id(
        callback_query.from_user.id,
        WorkerField.FULL_NAME.value
    )
    timetable = await get_timetable_from_google_sheet()
    row = await find_row_by_name_from_timetable(timetable, full_name)
    if row is None:
        await callback_query.message.edit_text(
            f"К сожалению Вас, {full_name}, в расписании не нашел, обратитесь к РОПу"
        )
        await show_main_menu(callback_query.message, worker_buttons)
        return

    shifts = await get_shifts(row)
    await callback_query.message.edit_text(
        await make_form(dict(zip(constants.week_abbreviated, shifts))),
        reply_markup=await make_inline_keyboard([OtherButton.CHANGE_SHIFT.value])
    )
    await state.set_state(ShiftChange.start)


async def get_timetable_from_google_sheet():
    result = google_sheets.service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="A1:I100",
        majorDimension="ROWS"
    ).execute()
    return result.get("values")


async def find_row_by_name_from_timetable(timetable: list, name: str):
    row = None
    for row in timetable:
        if name in row:
            row = row
    return row


async def get_shifts(row: list):
    shifts = row.copy()
    shifts.pop(0)
    return shifts
