import sqlite3


async def delete(database_name: str, table_name: str, condition: str, parameter):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", (parameter,))
    connection.commit()
    connection.close()
