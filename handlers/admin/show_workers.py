from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.buttons.data_buttons import admin_buttons, worker_settings_buttons
from UI.buttons.enums import ButtonWorkerSetting
from UI.buttons.enums.main_menu import AdminButton
from UI.methods import show_main_menu, make_inline_keyboard
from data import constants
from database.database_config import database_name, table_workers, table_queries
from database.enums import WorkerField, QueryField
from filters import IsAdmin, IsPrivate
from handlers.admin.add_worker import has_message_text
from utils import sql, generate_key, make_form


class ActionOnWorker(StatesGroup):
    worker_id = State()
    selecting_setting = State()
    selecting_parameter = State()
    changing_parameter = State()
    full_name = State()
    number_hours = State()
    number_weekend = State()


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.SHOW_WORKERS.value)
async def show_workers(callback_query: types.CallbackQuery, state: FSMContext):
    result = await sql.select(
        database_name,
        table_workers,
        columns=[WorkerField.FULL_NAME.value, WorkerField.ID.value]
    )
    if len(result) == 0:
        await callback_query.message.edit_text(constants.NO_WORKERS)
        await show_main_menu(callback_query.message, admin_buttons)
        return

    workers = dict(result)

    await callback_query.message.edit_text(
        constants.LIST_WORKERS,
        reply_markup=await make_inline_keyboard(workers)
    )
    await state.set_state(ActionOnWorker.worker_id)


@router.callback_query(StateFilter(ActionOnWorker.worker_id), IsAdmin())
async def take_worker_id(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data({WorkerField.ID.value: int(callback_query.data)})
        await callback_query.message.edit_text(
            constants.WORKER_SETTINGS,
            reply_markup=await make_inline_keyboard(worker_settings_buttons)
        )
        await state.set_state(ActionOnWorker.selecting_setting)
    except Exception:
        return


async def delete_worker_queries(worker_id):
    await sql.delete(
        database_name,
        table_queries,
        f"{QueryField.WORKER_ID.value} = ?",
        (worker_id,)
    )


@router.callback_query(
    StateFilter(ActionOnWorker.selecting_setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.DELETE_WORKER.value
)
async def delete_worker_and_his_queries(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    worker_id = user_data[WorkerField.ID.value]
    await sql.delete(
        database_name,
        table_workers,
        f"{WorkerField.ID.value} = ?",
        (worker_id,)
    )
    await delete_worker_queries(worker_id)
    await callback_query.message.edit_text(constants.REMOVE_WORKER)
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(ActionOnWorker.selecting_setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.RESET_USER.value
)
async def reset_user(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    key = await generate_key(constants.KEY_LENGTH)
    await sql.execute(
        database_name,
        f"UPDATE {table_workers} SET "
        f"{WorkerField.TELEGRAM_ID.value} = ?,"
        f"{WorkerField.USER_NAME.value} = ?,"
        f"{WorkerField.KEY.value} = ?"
        f"WHERE {WorkerField.ID.value} = ?",
        (None, None, key, user_data[WorkerField.ID.value],)
    )

    await callback_query.message.edit_text(f"{constants.RESET_USER_DATA}\n\nКлюч: {key}")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


async def make_keyboard_for_parameters_edition():
    data = [
        WorkerField.FULL_NAME.value,
        WorkerField.NUMBER_HOURS.value,
        WorkerField.NUMBER_WEEKEND.value
    ]
    buttons = {}
    for item in data:
        buttons.update({constants.descriptions_worker_parameters[item]: item})
    return await make_inline_keyboard(buttons)


@router.callback_query(
    StateFilter(ActionOnWorker.selecting_setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.CHANGE_PARAMETER.value
)
async def show_parameters(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    worker = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.ID.value} = ?",
        (user_data[WorkerField.ID.value],),
        list(constants.descriptions_worker_parameters.keys())
    )

    form_parameters = await make_form(
        dict(zip(constants.descriptions_worker_parameters.values(), worker[0])))

    await callback_query.message.edit_text(
        constants.PARAMETERS_WORKER + form_parameters,
        reply_markup=await make_keyboard_for_parameters_edition()
    )
    await state.set_state(ActionOnWorker.selecting_parameter)


reply_message = {
    WorkerField.FULL_NAME.value:
        {"message": constants.ENTER_FULL_NAME, "state": ActionOnWorker.full_name},
    WorkerField.NUMBER_HOURS.value:
        {"message": constants.ENTER_NUMBER_HOURS, "state": ActionOnWorker.number_hours},
    WorkerField.NUMBER_WEEKEND.value:
        {"message": constants.ENTER_NUMBER_WEEKEND, "state": ActionOnWorker.number_weekend},
}


@router.callback_query(
    StateFilter(ActionOnWorker.selecting_parameter),
    IsAdmin()
)
async def send_reply_message(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        value = reply_message[callback_query.data]
        await state.set_state(value["state"])
        await state.update_data({"name_parameter": callback_query.data})
        await callback_query.message.edit_text(value["message"])
    except Exception:
        return


@router.message(IsPrivate(), IsAdmin(), StateFilter(ActionOnWorker.full_name))
@has_message_text
async def take_full_name(message: types.Message, state: FSMContext):
    await state.update_data({"parameter": message.text})
    await update_parameter(message, state)


@router.message(IsPrivate(), IsAdmin(), StateFilter(ActionOnWorker.number_hours))
@has_message_text
async def take_number_hours(message: types.Message, state: FSMContext):
    try:
        number_hours = int(message.text)
    except Exception:
        raise ValueError(constants.INVALID_INPUT)

    if constants.MIN_NUMBER_HOURS <= number_hours <= constants.MAX_NUMBER_HOURS:
        await state.update_data({"parameter": number_hours})
        await update_parameter(message, state)
    else:
        raise ValueError(constants.INVALID_NUMBER_HOURS)


@router.message(IsPrivate(), IsAdmin(), StateFilter(ActionOnWorker.number_weekend))
@has_message_text
async def take_number_weekend(message: types.Message, state: FSMContext):
    try:
        number_weekend = int(message.text)
    except Exception:
        raise ValueError(constants.INVALID_INPUT)

    if constants.MIN_NUMBER_WEEKEND <= number_weekend <= constants.MAX_NUMBER_WEEKEND:
        await state.update_data({"parameter": number_weekend})
        await update_parameter(message, state)
    else:
        raise ValueError(constants.INVALID_NUMBER_WEEKEND)


async def update_parameter(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await sql.execute(
        database_name,
        f"UPDATE {table_workers} SET "
        f"{user_data['name_parameter']} = ?"
        f"WHERE {WorkerField.ID.value} = ?",
        (user_data['parameter'], user_data[WorkerField.ID.value])
    )
    await message.answer(constants.PARAMETER_CHANGED)
    await show_main_menu(message)
    await state.clear()
