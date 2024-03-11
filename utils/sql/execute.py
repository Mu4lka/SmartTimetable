import sqlite3


async def execute(database: str, sql: str, parameters: tuple = None):
    connection = sqlite3.connect(f"{database}.db")
    cursor = connection.cursor()
    if parameters is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, parameters)
        connection.commit()
    cursor.close()
    return cursor
