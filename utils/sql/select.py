import sqlite3


async def select(database_name: str, table_name: str, condition: str = None, parameter=None, columns: list[str] = None):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    sql_columns = "*"

    if columns is not None:
        sql_columns = f"{','.join([column for column in columns])}"

    if condition is None:
        cursor.execute(f"SELECT {sql_columns} FROM {table_name}")
    else:
        cursor.execute(f"SELECT {sql_columns} FROM {table_name} WHERE {condition}", (parameter,))
    result = cursor.fetchall()
    connection.close()
    return result
