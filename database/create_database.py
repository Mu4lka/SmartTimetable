import sqlite3

from database.database_config import database_name, table_workers, table_queries
from database.enums import DatabaseField, QueryField


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
        {DatabaseField.NUMBER_HOURS.value} INTEGER,
        {DatabaseField.NUMBER_WEEKEND.value} INTEGER)'''
    )
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_queries}(
            {QueryField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
            {QueryField.ID_TELEGRAM.value} INTEGER,
            {QueryField.TYPE.value} TEXT,
            {QueryField.QUERY_TEXT.value} TEXT)'''
    )
    connection.commit()
    connection.close()
    