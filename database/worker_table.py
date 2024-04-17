from enum import Enum

from utils.ease_sql import Table, Database


class WorkerField(str, Enum):
    ID = "worker_id"
    FULL_NAME = "full_name"
    USER_NAME = "user_name"
    TELEGRAM_ID = "telegram_id"
    KEY = "key"
    NUMBER_HOURS = "number_hours"
    NUMBER_WEEKEND = "number_weekend"


class WorkerTable(Table):
    name = "Workers"
    fields = (f"{WorkerField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,"
              f"{WorkerField.FULL_NAME.value} TEXT,"
              f"{WorkerField.USER_NAME.value} TEXT,"
              f"{WorkerField.TELEGRAM_ID.value} INTEGER,"
              f"{WorkerField.KEY.value} TEXT,"
              f"{WorkerField.NUMBER_HOURS.value} INTEGER,"
              f"{WorkerField.NUMBER_WEEKEND.value} INTEGER")

    def __init__(self, database: Database):
        super().__init__(self.name, database, self.fields)

    async def check_key(self, key: str, telegram_id: int, user_name: str):
        result = await self.select(
            f"{WorkerField.KEY.value}= ?",
            (key,),
            columns=[WorkerField.TELEGRAM_ID.value]
        )
        if len(result) == 0 or result[0][0] is not None:
            return False

        await self.update(
            [WorkerField.TELEGRAM_ID.value, WorkerField.USER_NAME.value],
            f"{WorkerField.KEY.value} = ?",
            (telegram_id, user_name, key,)
        )
        return True

    async def get_authorized(self, columns: list[str] = None):
        result = await self.select(
            f"{WorkerField.TELEGRAM_ID.value} IS NOT NULL", (),
            columns
        )
        return dict(result)

    async def get_values_by_telegram_id(self, telegram_id: int, columns: list[str]):
        result = await self.select(
            f"{WorkerField.TELEGRAM_ID.value} = ?",
            (telegram_id,),
            columns
        )
        return result[0][0]

    async def worker_number(self, worker_id):
        result = await self.select()
        index = 0
        for worker in result:
            if worker_id in worker:
                return index
            index += 1
