
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
from filters import IsAdmin
from utils import sql, generate_key


class ActionOnWorker(StatesGroup):
    worker_id = State()
    setting = State()


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
    except Exception:
        return
    await callback_query.message.edit_text(
        constants.WORKER_SETTINGS,
        reply_markup=await make_inline_keyboard(worker_settings_buttons)
    )
    await state.set_state(ActionOnWorker.setting)


async def delete_worker_queries(worker_id):
    await sql.delete(
        database_name,
        table_queries,
        f"{QueryField.WORKER_ID.value} = ?",
        (worker_id,)
    )


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
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
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.RESTORE_ACCESS.value
)
async def restore_access(callback_query: types.CallbackQuery, state: FSMContext):
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

    await callback_query.message.edit_text(f"{constants.ACCESS_RESTORED}\n\nКлюч: {key}")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()


@router.callback_query(
    StateFilter(ActionOnWorker.setting),
    IsAdmin(),
    F.data == ButtonWorkerSetting.EDIT_PARAMETERS.value
)
async def edit_parameters(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    worker = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.ID.value} = ?",
        (user_data[WorkerField.ID.value],)
    )
    print(list(worker[0]))
    await callback_query.message.answer(f"Редактирование параметров. Параметры")
    await show_main_menu(callback_query.message, admin_buttons)
    await state.clear()
