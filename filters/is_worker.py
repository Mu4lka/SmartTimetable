from aiogram import types
from aiogram.filters import Filter

from database.database_config import database_name, table_workers
from enums.database_field import DatabaseField
from utils.sql.select import select


class IsWorker(Filter):
    async def __call__(self, message: types.Message, user_id: int = None):
        if user_id is None:
            user_id = message.from_user.id

        result = await select(
            database_name,
            table_workers,
            f"{DatabaseField.ID_TELEGRAM.value} = ?",
            user_id
        )
        return not len(result) == 0
