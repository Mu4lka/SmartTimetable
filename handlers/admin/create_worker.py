from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.data_buttons import admin_buttons
from UI.get_message_parameters import get_message_parameters
from UI.show_main_menu import show_main_menu
from utils.generate_key import generate_key
from utils.sql.insert import insert
from enums.database_field import DatabaseField
from enums.menu import AdminButton
from filters.is_admin import IsAdmin
from data import constants
from UI.make_inline_keyboard import make_inline_keyboard


class CreatingWorker(StatesGroup):
    name = State()
    shift_duration = State()
    early_shift_start = State()
    late_shift_start = State()
    priority = State()
    efficiency = State()
    weekend = State()
    possible_weekend = State()


router = Router()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == AdminButton.CREATE_WORKER.value)
async def create_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(constants.ENTER_NAME)
    await state.set_state(CreatingWorker.name)


@router.message(IsAdmin(), StateFilter(CreatingWorker.name))
async def take_name(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    await state.update_data(name=message.text)
    await message.answer(constants.ENTER_SHIFT_DURATION)
    await state.set_state(CreatingWorker.shift_duration)


@router.message(IsAdmin(), StateFilter(CreatingWorker.shift_duration))
async def take_shift_duration(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        if int(message.text) > constants.MAX_SHIFT_DURATION:
            await message.answer(constants.INVALID_SHIFT_LENGTH)
            return
        await state.update_data(shift_duration=int(message.text))
    except ValueError:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_EARLY_SHIFT_START)
    await state.set_state(CreatingWorker.early_shift_start)


@router.message(IsAdmin(), StateFilter(CreatingWorker.early_shift_start))
async def take_early_shift_start(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        await state.update_data(early_shift_start=int(message.text))
    except ValueError:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_LATE_SHIFT_START)
    await state.set_state(CreatingWorker.late_shift_start)


@router.message(IsAdmin(), StateFilter(CreatingWorker.late_shift_start))
async def take_late_shift_start(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        user_data = await state.get_data()
        if int(message.text) < user_data[DatabaseField.EARLY_SHIFT_START]:
            await message.answer(constants.INVALID_LATE_START_SHIFT)
            return
        await state.update_data(late_shift_start=int(message.text))
    except ValueError:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_PRIORITY)
    await state.set_state(CreatingWorker.priority)


@router.message(IsAdmin(), StateFilter(CreatingWorker.priority))
async def take_priority(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        await state.update_data(priority=int(message.text))
    except ValueError:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(
        constants.SELECT_EFFICIENCY,
        reply_markup=await make_inline_keyboard(constants.efficiency)
    )
    await state.set_state(CreatingWorker.efficiency)


@router.callback_query(IsAdmin(), StateFilter(CreatingWorker.efficiency))
async def take_efficiency(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(efficiency=constants.efficiency.index(callback_query.data) + 1)
    except ValueError:
        return

    await callback_query.message.edit_text(
        constants.SELECT_WEEKEND,
        reply_markup=await make_inline_keyboard(constants.week_menu)
    )
    week_menu = []
    week_menu.extend(constants.week_menu)
    await state.update_data(week_menu=week_menu)
    await state.update_data(possible_weekend="")
    await state.set_state(CreatingWorker.weekend)


@router.callback_query(IsAdmin(), StateFilter(CreatingWorker.weekend))
async def take_weekend(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if not callback_query.data == constants.further:
        await update_possible_weekend(constants.SELECT_WEEKEND, callback_query, state)
        return

    possible_weekend = user_data[DatabaseField.POSSIBLE_WEEKEND.value]
    if len(possible_weekend) == 0:
        await state.update_data(weekend=len(possible_weekend))
        await add_worker_in_database(callback_query, state)
        return

    await state.update_data(weekend=len(possible_weekend))
    await callback_query.message.edit_text(
        constants.SELECT_POSSIBLE_WEEKEND,
        reply_markup=await make_inline_keyboard(user_data["week_menu"])
    )
    await state.set_state(CreatingWorker.possible_weekend)


@router.callback_query(IsAdmin(), StateFilter(CreatingWorker.possible_weekend))
async def take_possible_weekend(callback_query: types.CallbackQuery, state: FSMContext):
    if not callback_query.data == constants.further:
        await update_possible_weekend(constants.SELECT_POSSIBLE_WEEKEND, callback_query, state)
        return

    await add_worker_in_database(callback_query, state)


async def update_possible_weekend(message: str, callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    week_menu = user_data["week_menu"]
    await state.update_data(
        possible_weekend=user_data[DatabaseField.POSSIBLE_WEEKEND.value] +
        str(constants.week_menu.index(callback_query.data))
    )
    week_menu.remove(callback_query.data)
    await callback_query.message.edit_text(
        message,
        reply_markup=await make_inline_keyboard(week_menu)
    )
    await state.update_data(week_menu=week_menu)


async def add_worker_in_database(callback_query: types.CallbackQuery, state: FSMContext):
    from database.database_config import database_name, table_workers

    await state.update_data(key=await generate_key())
    user_data = await state.get_data()
    user_data.pop("week_menu")

    await insert(database_name, table_workers, user_data)

    await callback_query.message.edit_text(
        constants.ABOUT_CREATING_WORKER +
        await get_message_parameters(constants.descriptions_worker_parameters, user_data) +
        constants.ABOUT_SENDING_KEY_TO_WORKER
    )

    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()
