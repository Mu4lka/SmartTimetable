import asyncio

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu
from data import constants
from database.enums import WorkerField
from database.methods import get_worker_parameter_by_telegram_id
from filters import IsWorker
from google_sheets.methods import get_timetable
from utils import make_form
from utils.google_sheets.enums import Dimension

router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SHOW_MY_TIMETABLE.value)
async def show_worker_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    full_name = await get_worker_parameter_by_telegram_id(
        callback_query.from_user.id,
        WorkerField.FULL_NAME.value
    )
    timetable = await get_timetable_processing_error(Dimension.ROWS)
    row = await find_row_by_name_from_timetable(timetable, full_name)
    if row is None:
        await callback_query.message.edit_text(
            f"К сожалению Вас, {full_name}, в расписании не нашел, обратитесь к РОПу"
        )
        await show_main_menu(callback_query.message, worker_buttons)
        return
    shifts = await get_shifts(row)
    await callback_query.message.edit_text(
        "Ваше расписание:\n\n"
        f"<pre>{await make_form(dict(zip(constants.week_abbreviated, shifts)))}</pre>",
        parse_mode="HTML"
    )
    await show_main_menu(callback_query.message, worker_buttons)


async def get_timetable_processing_error(dimension: Dimension):
    try:
        return await get_timetable(dimension)
    except Exception:
        await asyncio.sleep(0.2)
        return await get_timetable_processing_error(dimension)


async def find_row_by_name_from_timetable(timetable: list, name: str):
    for row in timetable:
        if name in row:
            return row


async def get_shifts(row: list):
    shifts = row.copy()
    shifts.pop(0)
    return shifts
