import sqlite3


async def select(database_name: str, table_name: str, condition: str, parameter):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}", (parameter,))
    results = cursor.fetchall()
    connection.close()
    return results
