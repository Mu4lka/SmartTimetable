import sqlite3

from database.database_config import database_name, table_workers
from enums.database_field import DatabaseField
from utils.sql.select import select


async def check_key(key: str, user_id: int, user_name: str):
    results = await select(database_name, table_workers, f"{DatabaseField.KEY.value}= ?", key)

    if len(results) == 0:
        return False

    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {table_workers} SET "
                   f"{DatabaseField.ID_TELEGRAM.value} = ?,"
                   f"{DatabaseField.USER_NAME.value} = ?"
                   f"WHERE {DatabaseField.KEY.value} = ?",
                   (user_id, user_name, key,))
    connection.commit()
    connection.close()
    return True
