from aiogram import types
from aiogram.filters import Filter

from database.database_config import database_name, table_workers
from database.enums import WorkerField
from database.methods import found_from_database
from utils import sql


class IsWorker(Filter):
    async def __call__(self, message: types.Message, user_id: int = None):
        if user_id is None:
            user_id = message.from_user.id

        if message.from_user.is_bot:
            raise Exception("Данные принадлежат сущности 'Бот'")

        if await found_from_database(
                table_workers,
                f"{WorkerField.TELEGRAM_ID.value} = ? OR {WorkerField.USER_NAME.value} = ?",
                (user_id, message.from_user.username)):
            await sql.execute(
                database_name,
                f"UPDATE {table_workers} SET "
                f"{WorkerField.TELEGRAM_ID.value} = ?,"
                f"{WorkerField.USER_NAME.value} = ?"
                f"WHERE {WorkerField.TELEGRAM_ID.value} = ? OR {WorkerField.USER_NAME.value} = ?",
                (user_id, message.from_user.username, user_id, message.from_user.username,)
            )
            return True
        return False
