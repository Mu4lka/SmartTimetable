from typing import Any

from database.database_config import database_name, table_workers
from utils import sql


async def found_from_database(condition: str, parameter: Any):
    result = await sql.select(
        database_name,
        table_workers,
        condition,
        parameter
    )
    return not len(result) == 0
