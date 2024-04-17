from data import constants
from database import WorkerField
from loader import bot, worker_table
from utils.methods import make_form


async def notify_change(timetable_row: list):
    workers = await worker_table.get_authorized(
        [WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
    )
    telegram_id = workers[timetable_row.pop(0)]
    await bot.send_message(
        telegram_id,
        "Ваше расписание изменилось!\nТекущее расписание:\n\n"
        f"<pre>{await make_form(dict(zip(constants.week_abbreviated, timetable_row)))}</pre>",
        parse_mode="HTML"
    )
