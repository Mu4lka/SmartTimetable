from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from UI.data_buttons import admin_buttons, worker_settings_buttons
from UI.make_inline_keyboard import make_inline_keyboard
from UI.show_main_menu import show_main_menu
from data import constants
from database.database_config import table_workers, database_name
from enums.database_field import DatabaseField
from enums.main_menu import AdminButton
from enums.button_worker_setting import ButtonWorkerSetting
from filters.is_admin import IsAdmin
from utils.generate_key import generate_key
from utils.sql.delete import delete
from utils.sql.execute import execute
from utils.sql.select import select


class ActionOnWorker(StatesGroup):
    worker_id = State()
    setting = State()


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.SHOW_WORKERS.value)
async def show_workers(callback_query: types.CallbackQuery, state: FSMContext):
    result = await select(
        database_name,
        table_workers,
        columns=[DatabaseField.FULL_NAME.value, DatabaseField.ID.value]
    )
    if len(result) == 0:
        await callback_query.message.edit_text(constants.NO_WORKERS)
        await show_main_menu(callback_query.message, admin_buttons)
        return

    workers = {}
    for worker in result:
        workers.update({str(worker[0]): str(worker[1])})

    await callback_query.message.edit_text(
        constants.LIST_WORKERS,
        reply_markup=await make_inline_keyboard(workers)
    )
    await state.set_state(ActionOnWorker.worker_id)


@router.callback_query(StateFilter(ActionOnWorker.worker_id), IsAdmin())
async def take_worker_id(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(id=int(callback_query.data))
    except Exception:
        return
    await callback_query.message.edit_text(
        constants.WORKER_SETTINGS,
        reply_markup=await make_inline_keyboard(worker_settings_buttons)
    )
    await state.set_state(ActionOnWorker.setting)


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.DELETE_WORKER.value
)
async def delete_worker(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await delete(
        database_name,
        table_workers,
        f"{DatabaseField.ID.value} = ?",
        user_data[DatabaseField.ID.value]
    )

    await callback_query.message.edit_text(constants.REMOVE_WORKER)
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.RESTORE_ACCESS.value
)
async def restore_access(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    key = await generate_key(constants.KEY_LENGTH)
    await execute(
        database_name,
        f"UPDATE {table_workers} SET "
        f"{DatabaseField.ID_TELEGRAM.value} = ?,"
        f"{DatabaseField.USER_NAME.value} = ?,"
        f"{DatabaseField.KEY.value} = ?"
        f"WHERE {DatabaseField.ID.value} = ?",
        (None, None, key, user_data[DatabaseField.ID.value],)
    )

    await callback_query.message.answer(f"{constants.ACCESS_RESTORED}\n\nКлюч: {key}")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.EDIT_PARAMETERS.value
)
async def edit_parameters(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    worker = await select(
        database_name,
        table_workers,
        f"{DatabaseField.ID.value} = ?",
        user_data[DatabaseField.ID.value]
    )
    print(list(worker[0]))
    await callback_query.message.answer(f"Редактирование параметров. Параметры")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()
