from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.data_buttons import admin_buttons
from UI.make_text_parameters import make_text_parameters
from UI.show_main_menu import show_main_menu
from enums.other_button import OtherButton
from utils.generate_key import generate_key
from utils.sql.insert import insert
from enums.database_field import DatabaseField
from enums.main_menu import AdminButton
from filters.is_admin import IsAdmin
from data import constants
from UI.make_inline_keyboard import make_inline_keyboard


class CreatingWorker(StatesGroup):
    name = State()
    creation_type = State()
    shift_duration = State()
    early_shift_start = State()
    late_shift_start = State()
    priority = State()
    efficiency = State()
    weekend = State()
    possible_weekend = State()


router = Router()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == AdminButton.CREATE_WORKER.value)
async def start_creating_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(constants.ENTER_NAME)
    await state.set_state(CreatingWorker.name)


@router.message(IsAdmin(), StateFilter(CreatingWorker.name))
async def take_name(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    await state.update_data({DatabaseField.NAME.value: message.text})
    await message.answer(
        constants.SELECT_CREATION_TYPE,
        reply_markup=await make_inline_keyboard([
            OtherButton.QUICKLY_CREATE.value,
            OtherButton.CREATE_MANUALLY.value
        ]))
    await state.set_state(CreatingWorker.creation_type)


@router.callback_query(
    IsAdmin(),
    StateFilter(CreatingWorker.creation_type),
    F.data == OtherButton.QUICKLY_CREATE.value
)
async def create_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data({
        DatabaseField.SHIFT_DURATION.value: 8,
        DatabaseField.EARLY_SHIFT_START.value: 8,
        DatabaseField.LATE_SHIFT_START.value: 10,
        DatabaseField.PRIORITY.value: 0,
        DatabaseField.EFFICIENCY.value: 2,
        DatabaseField.WEEKEND.value: 2,
        DatabaseField.POSSIBLE_WEEKEND.value: "456",
    })
    await add_worker_in_database(callback_query, state)


@router.callback_query(
    IsAdmin(),
    StateFilter(CreatingWorker.creation_type),
    F.data == OtherButton.CREATE_MANUALLY.value
)
async def continue_creating_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(constants.ENTER_SHIFT_DURATION)
    await state.set_state(CreatingWorker.shift_duration)


@router.message(IsAdmin(), StateFilter(CreatingWorker.shift_duration))
async def take_shift_duration(message: types.Message, state: FSMContext):
    try:
        shift_duration = int(message.text)
        if (shift_duration < constants.MIN_SHIFT_DURATION or
                shift_duration > constants.MAX_SHIFT_DURATION):
            await message.answer(constants.INVALID_SHIFT_LENGTH)
            return
        await state.update_data({DatabaseField.SHIFT_DURATION.value: shift_duration})
    except Exception:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_EARLY_SHIFT_START)
    await state.set_state(CreatingWorker.early_shift_start)


@router.message(IsAdmin(), StateFilter(CreatingWorker.early_shift_start))
async def take_early_shift_start(message: types.Message, state: FSMContext):
    try:
        early_shift_start = int(message.text)
        if (early_shift_start < constants.DAY_START or
                early_shift_start > constants.DAY_END):
            await message.answer(constants.INVALID_EARLY_SHIFT_START)
            return
        await state.update_data({DatabaseField.EARLY_SHIFT_START.value: early_shift_start})
    except Exception:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_LATE_SHIFT_START)
    await state.set_state(CreatingWorker.late_shift_start)


@router.message(IsAdmin(), StateFilter(CreatingWorker.late_shift_start))
async def take_late_shift_start(message: types.Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        late_shift_start = int(message.text)
        if (late_shift_start < user_data[DatabaseField.EARLY_SHIFT_START] or
                late_shift_start > constants.DAY_END):
            await message.answer(constants.INVALID_LATE_START_SHIFT)
            return
        await state.update_data({DatabaseField.LATE_SHIFT_START.value: late_shift_start})
    except Exception:
        await message.answer(constants.INVALID_INPUT)
        return

    await message.answer(constants.ENTER_PRIORITY)
    await state.set_state(CreatingWorker.priority)


@router.message(IsAdmin(), StateFilter(CreatingWorker.priority))
async def take_priority(message: types.Message, state: FSMContext):
    try:
        await state.update_data({DatabaseField.PRIORITY.value: int(message.text)})
    except Exception:
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
        await state.update_data(
            {DatabaseField.EFFICIENCY.value: constants.efficiency.index(callback_query.data) + 1}
        )
    except Exception:
        return

    week_menu = []
    week_menu.extend(constants.week_menu)
    await state.update_data(week_menu=week_menu)
    await state.update_data({DatabaseField.POSSIBLE_WEEKEND.value: ""})

    await callback_query.message.edit_text(
        constants.SELECT_WEEKEND,
        reply_markup=await make_inline_keyboard(constants.week_menu)
    )
    await state.set_state(CreatingWorker.weekend)


@router.callback_query(IsAdmin(), StateFilter(CreatingWorker.weekend))
async def take_weekend(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if not callback_query.data == constants.further:
        await update_possible_weekend(constants.SELECT_WEEKEND, callback_query, state)
        return

    possible_weekend = user_data[DatabaseField.POSSIBLE_WEEKEND.value]
    if len(possible_weekend) == 0:
        await state.update_data({DatabaseField.WEEKEND.value: 0})
        await add_worker_in_database(callback_query, state)
        return

    await state.update_data({DatabaseField.WEEKEND.value: len(possible_weekend)})

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
    try:
        week_menu.remove(callback_query.data)
        await state.update_data(
            {DatabaseField.POSSIBLE_WEEKEND.value:
                 (user_data[DatabaseField.POSSIBLE_WEEKEND.value] +
                  str(constants.week_menu.index(callback_query.data)))}
        )
    except Exception:
        pass

    await callback_query.message.edit_text(
        message,
        reply_markup=await make_inline_keyboard(week_menu)
    )
    await state.update_data(week_menu=week_menu)


async def add_worker_in_database(callback_query: types.CallbackQuery, state: FSMContext):
    from database.database_config import database_name, table_workers

    await state.update_data(key=await generate_key(constants.KEY_LENGTH))
    user_data = await state.get_data()

    try:
        user_data.pop("week_menu")
    except Exception:
        pass

    await insert(database_name, table_workers, user_data)
    await callback_query.message.edit_text(
        constants.ABOUT_CREATING_WORKER +
        await make_text_parameters(constants.descriptions_worker_parameters, user_data) +
        constants.ABOUT_SENDING_KEY_TO_WORKER
    )

    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()
