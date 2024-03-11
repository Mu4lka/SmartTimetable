import sqlite3


async def select(
        database: str,
        table_name: str,
        condition: str = None,
        parameters: tuple = None,
        columns: list[str] = None):
    with sqlite3.connect(f"{database}.db") as connection:
        cursor = connection.cursor()
        sql_columns = "*" if columns is None else ",".join(columns)

        if condition is None:
            cursor.execute(f"SELECT {sql_columns} FROM {table_name}")
        else:
            cursor.execute(
                f"SELECT {sql_columns} FROM {table_name} WHERE {condition}",
                parameters
            )
        result = cursor.fetchall()
    return result
