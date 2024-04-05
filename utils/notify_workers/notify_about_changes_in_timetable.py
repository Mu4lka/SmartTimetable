from typing import Union

from loader import bot


def get_worker_ids_to_notify(timetable: Union[list, None], current_timetable: list, workers: dict):
    worker_ids = []
    for item in range(len(current_timetable)):
        try:
            if timetable[item] != current_timetable[item]:
                try:
                    worker_id = workers[current_timetable[item][0]]
                    worker_ids.append(worker_id)
                except Exception:
                    continue
        except Exception:
            continue
    return set(worker_ids)


async def notify_about_changes_in_timetable(timetable: Union[list, None], current_timetable: list, workers: dict):
    if timetable is None:
        return

    for worker_id in get_worker_ids_to_notify(timetable, current_timetable, workers):
        await send_changes_in_timetable_message(worker_id)



async def send_changes_in_timetable_message(worker_id):
    message_text = f"Ваше расписание на этой неделе было изменено..."
    await bot.send_message(worker_id, message_text)
