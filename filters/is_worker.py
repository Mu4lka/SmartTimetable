from aiogram import types
from aiogram.filters import Filter

from database.database_config import database_name, table_workers
from database.enums import DatabaseField
from database.methods import found_from_database
from utils import sql


class IsWorker(Filter):
    async def __call__(self, message: types.Message, user_id: int = None):
        if user_id is None:
            user_id = message.from_user.id

        if await found_from_database(
                f"{DatabaseField.ID_TELEGRAM.value} = ?",
                user_id):
            return True
        else:
            if await found_from_database(
                    f"{DatabaseField.USER_NAME.value} = ?",
                    message.from_user.username):
                await sql.execute(
                    database_name,
                    f"UPDATE {table_workers} SET "
                    f"{DatabaseField.ID_TELEGRAM.value} = ?"
                    f"WHERE {DatabaseField.USER_NAME.value} = ?",
                    (user_id, message.from_user.username)
                )
                return True
        return False
