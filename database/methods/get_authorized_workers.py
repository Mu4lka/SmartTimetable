from database.database_config import database_name, table_workers
from database.enums import WorkerField
from utils import sql


async def get_authorized_workers():
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.TELEGRAM_ID.value} IS NOT NULL", (),
        columns=[WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
    )
    return dict(result)
