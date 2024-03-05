from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.buttons.data_buttons import admin_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import make_inline_keyboard, make_text_parameters, show_main_menu
from data import constants
from database.enums import WorkerField
from filters import IsAdmin
from utils import generate_key, sql


class CreatingWorker(StatesGroup):
    full_name = State()
    number_hours = State()
    number_weekend = State()
    user_name = State()


router = Router()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == AdminButton.CREATE_WORKER.value)
async def start_creating_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(constants.ENTER_FULL_NAME)
    await state.set_state(CreatingWorker.full_name)


@router.message(IsAdmin(), StateFilter(CreatingWorker.full_name))
async def take_full_name(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    await state.update_data({WorkerField.FULL_NAME.value: message.text})
    await message.answer(constants.ENTER_NUMBER_HOURS)
    await state.set_state(CreatingWorker.number_hours)


@router.message(IsAdmin(), StateFilter(CreatingWorker.number_hours))
async def take_number_hours(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        number_hours = int(message.text)
        if constants.MIN_NUMBER_HOURS <= number_hours <= constants.MAX_NUMBER_HOURS:
            await state.update_data({WorkerField.NUMBER_HOURS.value: number_hours})
            await message.answer(constants.ENTER_NUMBER_WEEKEND)
            await state.set_state(CreatingWorker.number_weekend)
        else:
            await message.answer(constants.INVALID_NUMBER_HOURS)
    except Exception:
        await message.answer(constants.INVALID_INPUT)


@router.message(IsAdmin(), StateFilter(CreatingWorker.number_weekend))
async def take_number_weekend(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    try:
        number_weekend = int(message.text)
        if constants.MIN_NUMBER_WEEKEND <= number_weekend <= constants.MAX_NUMBER_WEEKEND:
            await state.update_data({WorkerField.NUMBER_WEEKEND.value: number_weekend})
            await message.answer(
                constants.ENTER_USER_NAME,
                reply_markup=await make_inline_keyboard([OtherButton.SKIP.value])
            )
            await state.set_state(CreatingWorker.user_name)
        else:
            await message.answer(constants.INVALID_NUMBER_WEEKEND)
    except Exception:
        await message.answer(constants.INVALID_INPUT)


@router.message(IsAdmin(), StateFilter(CreatingWorker.user_name))
async def take_user_name(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer(constants.INVALID_INPUT)
        return

    user_name = message.text.strip("@")
    telegram_link = "https://t.me/"
    if telegram_link in user_name:
        user_name = user_name.rsplit(telegram_link, 1)[1]
    await state.update_data({WorkerField.USER_NAME.value: user_name})
    await add_worker_in_database(message, state)


@router.callback_query(IsAdmin(), StateFilter(CreatingWorker.user_name), F.data == OtherButton.SKIP.value)
async def create_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await add_worker_in_database(callback_query.message, state)


async def add_worker_in_database(message: types.Message, state: FSMContext):
    from database.database_config import database_name, table_workers

    await state.update_data({WorkerField.KEY.value: await generate_key(constants.KEY_LENGTH)})
    user_data = await state.get_data()

    await sql.insert(database_name, table_workers, user_data)
    await message.answer(
        constants.ABOUT_CREATING_WORKER +
        await make_text_parameters(constants.descriptions_worker_parameters, user_data) +
        constants.ABOUT_SENDING_KEY_TO_WORKER
    )

    await show_main_menu(message, admin_buttons)
    await state.clear()
