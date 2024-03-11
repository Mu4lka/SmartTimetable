import sqlite3


async def delete(database: str, table_name: str, condition: str, parameters: tuple):
    with sqlite3.connect(f"{database}.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", parameters)
        connection.commit()
