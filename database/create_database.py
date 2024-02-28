import sqlite3

from database.database_config import database_name, table_workers
from database.enums import DatabaseField


def create_database():
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_workers}(
        {DatabaseField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
        {DatabaseField.FULL_NAME.value} TEXT,
        {DatabaseField.USER_NAME.value} TEXT,
        {DatabaseField.ID_TELEGRAM.value} INTEGER,
        {DatabaseField.KEY.value} TEXT,
        {DatabaseField.NUMBER_HOURS.value} INTEGER)'''
    )
    connection.commit()
    connection.close()
    