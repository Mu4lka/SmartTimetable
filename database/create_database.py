import sqlite3

from database.database_config import database_name, table_workers
from enums.database_field import DatabaseField


def create_database():
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_workers}(
        {DatabaseField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
        {DatabaseField.NAME.value} TEXT,
        {DatabaseField.USER_NAME.value} TEXT,
        {DatabaseField.ID_TELEGRAM.value} INTEGER,
        {DatabaseField.KEY.value} TEXT,
        {DatabaseField.SHIFT_DURATION.value} INTEGER,
        {DatabaseField.EARLY_SHIFT_START.value} INTEGER,
        {DatabaseField.LATE_SHIFT_START.value} INTEGER,
        {DatabaseField.EFFICIENCY.value} INTEGER,
        {DatabaseField.WEEKEND.value} INTEGER,
        {DatabaseField.POSSIBLE_WEEKEND.value} TEXT,
        {DatabaseField.PRIORITY.value} INTEGER)'''
    )
    connection.commit()
    connection.close()
    