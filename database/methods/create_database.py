from database.database_config import database_name, table_workers, table_queries
from database.enums import WorkerField, QueryField
from utils import sql


async def create_database():
    await sql.execute(
        database_name,
        f"""CREATE TABLE IF NOT EXISTS {table_workers}(
            {WorkerField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
            {WorkerField.FULL_NAME.value} TEXT,
            {WorkerField.USER_NAME.value} TEXT,
            {WorkerField.TELEGRAM_ID.value} INTEGER,
            {WorkerField.KEY.value} TEXT,
            {WorkerField.NUMBER_HOURS.value} INTEGER,
            {WorkerField.NUMBER_WEEKEND.value} INTEGER)"""
    )
    await sql.execute(
        database_name,
        f"""CREATE TABLE IF NOT EXISTS {table_queries}(
            {QueryField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,
            {QueryField.WORKER_ID.value} INTEGER,
            {QueryField.TYPE.value} TEXT,
            {QueryField.QUERY_TEXT.value} TEXT,
            FOREIGN KEY ({QueryField.WORKER_ID.value})
            REFERENCES {table_workers}({WorkerField.ID.value}))"""
    )
