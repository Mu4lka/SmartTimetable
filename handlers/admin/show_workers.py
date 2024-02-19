import sqlite3

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
from enums.menu import AdminButton
from enums.worker_setting import WorkerSetting
from filters.is_admin import IsAdmin
from utils.sql.delete import delete
from utils.sql.select import select


class ActionOnWorker(StatesGroup):
    id = State()
    setting = State()


router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == AdminButton.SHOW_WORKERS.value)
async def show_workers(callback_query: types.CallbackQuery, state: FSMContext):
    workers_names = await select(database_name, table_workers, columns=[DatabaseField.NAME.value])
    if len(workers_names) == 0:
        await callback_query.message.edit_text(constants.NO_WORKERS)
        await show_main_menu(callback_query.message, admin_buttons)
        return

    names = []
    for worker_name in workers_names:
        names.append(worker_name[0])

    await callback_query.message.edit_text(
        constants.LIST_WORKERS,
        reply_markup=await make_inline_keyboard(names, True)
    )
    await state.set_state(ActionOnWorker.id)


@router.callback_query(StateFilter(ActionOnWorker.id), IsAdmin())
async def take_worker_id(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(id=int(callback_query.data) + 1)
    await callback_query.message.edit_text(
        constants.WORKER_SETTINGS,
        reply_markup=await make_inline_keyboard(worker_settings_buttons)
    )
    await state.set_state(ActionOnWorker.setting)


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == WorkerSetting.DELETE_WORKER.value
)
async def delete_worker(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await delete(database_name,
                 table_workers,
                 f"{DatabaseField.ID.value} = ?",
                 user_data[DatabaseField.ID.value])

    await callback_query.message.edit_text(constants.REMOVE_WORKER)
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == WorkerSetting.EDIT_PARAMETERS.value
)
async def edit_parameters(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Редактирование параметров")
    pass


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == WorkerSetting.RESTORE_ACCESS.value
)
async def restore_access(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {table_workers} SET "
                   f"{DatabaseField.ID_TELEGRAM.value} = ?,"
                   f"{DatabaseField.USER_NAME.value} = ?"
                   f"WHERE {DatabaseField.ID.value} = ?",
                   (None, None, user_data[DatabaseField.ID.value],))
    connection.commit()
    connection.close()

    await callback_query.message.answer("Доступ восстановлен")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()
