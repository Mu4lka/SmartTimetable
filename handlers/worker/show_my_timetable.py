from aiogram import Router, F, types
from aiogram.filters import StateFilter

from UI.buttons.data_buttons import worker_buttons
from UI.buttons.enums.main_menu import WorkerButton
from UI.methods import show_main_menu
from data import constants
from database import WorkerField
from filters import IsWorker
from loader import timetable_storage, worker_table
from utils.methods import make_form

router = Router()


@router.callback_query(StateFilter(None), IsWorker(), F.data == WorkerButton.SHOW_MY_TIMETABLE.value)
async def show_worker_timetable(callback_query: types.CallbackQuery):
    full_name = await worker_table.get_values_by_telegram_id(
        callback_query.from_user.id,
        [WorkerField.FULL_NAME.value,]
    )
    element = await find_element_by_name_from_timetable(
        timetable_storage.get_timetable(),
        full_name
    )
    if element is None:
        text = f"К сожалению Вас, {full_name}, в расписании не нашел, обратитесь к руководителю!"
    else:
        text = (f"<b>Ваше расписание:</b>\n\n"
                f"<pre>{make_form(dict(zip(constants.week_abbreviated, await get_shifts(element))))}</pre>")
    await callback_query.message.edit_text(text, parse_mode="HTML")
    await show_main_menu(callback_query.message, worker_buttons)


async def find_element_by_name_from_timetable(timetable: list, name: str):
    for element in timetable:
        if name in element:
            return element


async def get_shifts(timetable_element: list):
    shifts = timetable_element.copy()
    shifts.pop(0)
    return shifts
