import sqlite3


async def execute(database_name: str, sql: str, parameters: tuple = None):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(sql, parameters)
    connection.commit()
    connection.close()
