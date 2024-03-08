from typing import Any

from database.database_config import database_name
from utils import sql


async def found_from_database(table_name: str, condition: str, parameter: Any):
    result = await sql.select(
        database_name,
        table_name,
        condition,
        parameter
    )
    return not len(result) == 0
