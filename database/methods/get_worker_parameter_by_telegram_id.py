from database.database_config import database_name, table_workers
from database.enums import WorkerField
from utils import sql


async def get_worker_parameter_by_telegram_id(user_id: int, parameter: str):
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.TELEGRAM_ID.value} = ?",
        (user_id,),
        [parameter]
    )
    return result[0][0]
