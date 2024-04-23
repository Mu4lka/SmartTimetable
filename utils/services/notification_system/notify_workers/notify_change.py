from data import constants
from database import WorkerField
from loader import bot, worker_table
from utils.methods import make_form


def get_differences(current_element: list, element: list):
    element.pop(0)
    max_length = 7
    current_element += ["Нет"] * (max_length - len(current_element))
    element += ["Нет"] * (max_length - len(element))
    differences = {}
    i = 0
    for item1, item2 in zip(element, current_element):
        if item1 != item2 and (not (item1 == "Нет" and item2 == "")):
            if item1 == "":
                item1 = "Нет"
            if item2 == "":
                item2 = "Нет"
            differences.update(
                {constants.week_abbreviated[i]: f"{item1} --> {item2}"}
            )
        i += 1
    return differences


async def notify_change(current_element: list, element: list, sheet_name):
    workers = await worker_table.get_authorized(
        [WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
    )
    telegram_id = workers[current_element.pop(0)]
    differences = get_differences(current_element.copy(), element.copy())
    await bot.send_message(
        telegram_id,
        f"<b>Ваше расписание на {sheet_name} изменилось!</b>\n\n"
        f"<b>Изменения:</b>\n"
        f"<pre>{make_form(differences, ': ')}</pre>\n"
        f"<b>Текущее расписание:</b>\n"
        f"<pre>{make_form(dict(zip(constants.week_abbreviated, current_element)))}</pre>",
        parse_mode="HTML"
    )
