from aiogram import types
from aiogram.filters import Filter

from database import WorkerField
from loader import worker_table


class IsWorker(Filter):
    async def __call__(self, message: types.Message, user_id: int = None):
        if user_id is None:
            user_id = message.from_user.id

        if message.from_user.is_bot:
            raise Exception("Данные принадлежат сущности 'Бот'")

        if await worker_table.found(
                f"{WorkerField.TELEGRAM_ID.value} = ? OR {WorkerField.USER_NAME.value} = ?",
                (user_id, message.from_user.username)):
            await worker_table.update(
                [WorkerField.TELEGRAM_ID.value, WorkerField.USER_NAME.value],
                f"{WorkerField.TELEGRAM_ID.value} = ? OR {WorkerField.USER_NAME.value} = ?",
                (user_id, message.from_user.username, user_id, message.from_user.username,)
            )
            return True
        return False
