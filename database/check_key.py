from database.database_config import database_name, table_workers
from enums.database_field import DatabaseField
from utils.sql.execute import execute
from utils.sql.select import select


async def check_key(key: str, user_id: int, user_name: str):
    result = await select(
        database_name,
        table_workers,
        f"{DatabaseField.KEY.value}= ?",
        key
    )

    if len(result) == 0:
        return False

    await execute(
        database_name,
        f"UPDATE {table_workers} SET "
        f"{DatabaseField.ID_TELEGRAM.value} = ?,"
        f"{DatabaseField.USER_NAME.value} = ?"
        f"WHERE {DatabaseField.KEY.value} = ?",
        (user_id, user_name, key,)
    )
    return True
