from typing import Union

from loader import bot


async def notify_about_changes_in_timetable(timetable: Union[list, None], current_timetable: list, workers: dict):
    if timetable is None:
        return

    for item in range(len(current_timetable)):
        try:
            if timetable[item] != current_timetable[item]:
                try:
                    worker_id = workers[current_timetable[item][0]]
                    await send_changes_in_timetable_message(worker_id)
                except Exception:
                    break
        except Exception:
            break


async def send_changes_in_timetable_message(worker_id):
    message_text = f"Ваше расписание на этой неделе было изменено..."
    await bot.send_message(worker_id, message_text)
