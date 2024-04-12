from data import constants
from database.methods import get_authorized_workers
from loader import bot
from utils.methods import make_form


async def notify_change(timetable_row: list):
    workers = await get_authorized_workers()
    worker_id = workers[timetable_row.pop(0)]
    await bot.send_message(
        worker_id,
        "Ваше расписание изменилось!\nТекущее расписание:\n\n"
        f"<pre>{await make_form(dict(zip(constants.week_abbreviated, timetable_row)))}</pre>",
        parse_mode="HTML"
    )
