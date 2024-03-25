from database.enums import WorkerField

DAY_START = 0
DAY_END = 24
MAX_SHIFT_DURATION = 20
KEY_LENGTH = 12

MIN_NUMBER_HOURS = 0
MAX_NUMBER_HOURS = 7 * MAX_SHIFT_DURATION

MIN_NUMBER_WEEKEND = 0
MAX_NUMBER_WEEKEND = 7

START_BOT = "Бот запущен"
MAIN_MENU = "Главное меню"

ABOUT_NOT_AUTHORIZED = "Введите ключ для авторизации вашего аккаунта"

# Adding worker
ADDING_WORKER = "Добавление сотрудника..."
ENTER_FULL_NAME = ("\nВведите полное имя (ИФ)...\n\n"
                   "Важно!!! Полное имя (ИФ) должно совпадать с расписанием")
ENTER_NUMBER_HOURS = "Введите количество часов в неделю"
ENTER_NUMBER_WEEKEND = "Введите количество выходных"
ENTER_USER_NAME = (f"(Не обязательно)\nВведите пользовательское имя...\n"
                   f"Например: имя_пользователя, @имя_пользователя или https://t.me/имя_пользователя")
ABOUT_ADDING_WORKER = "Вы добавили сотрудника!\nЕго параметры:\n\n"
ABOUT_SENDING_KEY_TO_WORKER = ("\nP.S. Вы можете отправить ключ сотруднику для его авторизации, "
                               "если вы не указали пользовательское имя сотрудника")

INVALID_NUMBER_HOURS = (f"Число вне диапазона!\n"
                        f"Число должно входить в диапазон от {MIN_NUMBER_HOURS} до {MAX_NUMBER_HOURS}.\n\n"
                        f"Попробуйте ещё раз...")

INVALID_NUMBER_WEEKEND = (f"Число вне диапазона!\n"
                          f"Число должно входить в диапазон от {MIN_NUMBER_WEEKEND} до {MAX_NUMBER_WEEKEND}.\n\n"
                          f"Попробуйте ещё раз...")

INVALID_INPUT = "Неверный формат ввода, попробуйте ещё раз..."

# Edition worker
LIST_WORKERS = "Список сотрудников"
WORKER_SETTINGS = "Настройки сотрудника"
PARAMETERS_WORKER = "Параметры сотрудника\n\n"
NO_WORKERS = "Нет сотрудников"
REMOVE_WORKER = "Вы удалили сотрудника"
RESET_USER_DATA = "Пользовательские данные сотрудника были сброшены, отправьте ключ для его повторной авторизации: "
PARAMETER_CHANGED = "Параметр изменен"

# making timetable
INVALID_ABOUT_MORE_THAN_ONE_SCHEDULE = "Вы уже отравляли расписание!"
INVALID_TIMETABLE = "Неверный формат расписания, попробуйте еще раз..."

NOT_AVAILABLE_YET = "пока не доступно"

NEW_TIMETABLE = "Новое расписание"

# other
week_russian = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
week_abbreviated = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

format_timetable = ["Сотрудник"] + week_russian + ["Общие часы (ч)"]

descriptions_worker_parameters = {
    WorkerField.FULL_NAME.value: "Имя",
    WorkerField.USER_NAME.value: "Пользовательское имя",
    WorkerField.TELEGRAM_ID.value: "Айди пользователя",
    WorkerField.KEY.value: "Ключ",
    WorkerField.NUMBER_HOURS.value: "Количество часов",
    WorkerField.NUMBER_WEEKEND.value: "Количество выходных"
}
day_off = "выходной"
EXAMPLE_TEMPLATE = (
    "Отправьте расписание используя шаблон...\n\n"
    f"<pre>пн: 8:00-18:00\n"
    f"вт: 09:30-18:30\n"
    f"ср: 10:00-18:00\n"
    f"чт: 10:00-18:30\n"
    f"пт: 10:00-18:00\n"
    f"сб: {day_off}\n"
    f"вс: {day_off}</pre>\n\n"
)