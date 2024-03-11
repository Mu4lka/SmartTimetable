import sqlite3
from typing import Any


async def insert(database: str, table_name: str, fields: dict[str, Any]):
    with sqlite3.connect(f"{database}.db") as connection:
        cursor = connection.cursor()
        columns = ",".join(fields.keys())
        placeholders = ",".join(["?" for _ in range(len(fields))])
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", list(fields.values()))
        connection.commit()
