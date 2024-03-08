import sqlite3

from database.database_config import database_name, table_workers, table_queries
from database.enums import WorkerField, QueryField


def create_database():
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_workers}(
        {WorkerField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
        {WorkerField.FULL_NAME.value} TEXT,
        {WorkerField.USER_NAME.value} TEXT,
        {WorkerField.USER_ID.value} INTEGER,
        {WorkerField.KEY.value} TEXT,
        {WorkerField.NUMBER_HOURS.value} INTEGER,
        {WorkerField.NUMBER_WEEKEND.value} INTEGER)'''
    )
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_queries}(
            {QueryField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
            {QueryField.USER_ID.value} INTEGER,
            {QueryField.TYPE.value} TEXT,
            {QueryField.QUERY_TEXT.value} TEXT)'''
    )
    connection.commit()
    connection.close()
    