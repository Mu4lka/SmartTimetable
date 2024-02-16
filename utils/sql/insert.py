import sqlite3


async def insert(database_name: str, table_name: str, fields: dict):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table_name} ({','.join([key for key in list(fields.keys())])})"
                   f"VALUES ({','.join([str('?') for _ in range(len(fields))])})",
                   list(fields.values()))
    connection.commit()
    connection.close()
