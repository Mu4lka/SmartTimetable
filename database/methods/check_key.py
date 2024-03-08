from database.database_config import database_name, table_workers
from database.enums import WorkerField
from utils import sql


async def check_key(key: str, user_id: int, user_name: str):
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.KEY.value}= ?",
        key,
        columns=[WorkerField.USER_ID.value]
    )
    if len(result) == 0 or result[0][0] is not None:
        return False

    await sql.execute(
        database_name,
        f"UPDATE {table_workers} SET "
        f"{WorkerField.USER_ID.value} = ?,"
        f"{WorkerField.USER_NAME.value} = ?"
        f"WHERE {WorkerField.KEY.value} = ?",
        (user_id, user_name, key,)
    )
    return True
