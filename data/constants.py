from enums.database_field import DatabaseField

DAY_START = 0
DAY_END = 24
MAX_SHIFT_DURATION = 16
KEY_LENGTH = 12

START_BOT = "Бот запущен"
SELECT_COMMAND = "Выберите команду..."
CANCEL = "Отменено"

ABOUT_NOT_AUTHORIZED = "Введите ключ для авторизации вашего аккаунта"
GREETINGS_TO_ADMIN = "Вы вошли под статусом \"Админ\""
GREETINGS_TO_WORKER = "Вы вошли под статусом \"Сотрудник\""
CAME_OUT = "Вы вышли!"

ENTER_NAME = "Создание сотрудника...\nВведите имя"
ENTER_SHIFT_DURATION = "Введите количество часов в смене"
ENTER_EARLY_SHIFT_START = "Введите раннее начало смены, то есть минимальное время для начала смены"
ENTER_LATE_SHIFT_START = "Введите позднее начало смены, то есть максимальное время для начала смены"
ENTER_PRIORITY = ("Введите число-приоритет (это число указывающее номер порядка, как будет происходить генерация для "
                  "расписания. От большего к меньшему. По умолчанию ноль)")
SELECT_EFFICIENCY = "Выберите эффективность"
SELECT_WEEKEND = \
    "Выберите дни недели для количества выходных, также они будут считаться как возможные выходные дни недели"
SELECT_POSSIBLE_WEEKEND = "Выберите дополнительные возможные выходные дни недели"
ABOUT_CREATING_WORKER = "Вы создали сотрудника! Его параметры:\n\n"
ABOUT_SENDING_KEY_TO_WORKER = "\nP.S. Отправьте ключ сотруднику, для его авторизации под статусом \"Сотрудник\"."

INVALID_INPUT = "Неверный формат ввода, попробуйте ещё раз..."
INVALID_SHIFT_LENGTH = (f"Недопустимая продолжительность смены, пожалейте работника ;) "
                        f"(задано ограничение {MAX_SHIFT_DURATION} часов). Введите еще раз...")
INVALID_LATE_START_SHIFT = ("Недопустимое позднее начало смены "
                            "(должно быть не меньше начало ранней смены). Введите еще раз...")
INVALID_REQUEST = "Неактуальный запрос"

LIST_WORKERS = "Список сотрудников. Выберите сотрудника чтобы его настроить"
WORKER_SETTINGS = "Настройки сотрудника. Выберите команду..."
PARAMETERS_WORKER = "Параметры сотрудника. Выберите параметр, который нужно изменить"
NO_WORKERS = "Нет сотрудников"
REMOVE_WORKER = "Вы удалили сотрудника"
LIMITATION_ON_NUMBER_WORKER = "Ограничение по количеству сотрудников"
ACCESS_RESTORED = "Доступ восстановлен. Теперь отправьте новый ключ сотруднику..."

NOT_AVAILABLE_YET = "пока не доступно"

week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
week_abbreviated = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
further = "Далее"
week_menu = week + [further]
efficiency = ["Стажер", "Средний", "Профессионал"]

descriptions_worker_parameters = {
    DatabaseField.NAME.value: 'Имя',
    DatabaseField.USER_NAME.value: 'Пользовательское имя',
    DatabaseField.ID_TELEGRAM.value: 'Айди пользователя',
    DatabaseField.KEY.value: 'Ключ',
    DatabaseField.SHIFT_DURATION.value: 'Продолжительность смены',
    DatabaseField.EARLY_SHIFT_START.value: 'Раннее начало смены',
    DatabaseField.LATE_SHIFT_START.value: 'Позднее начало смены',
    DatabaseField.EFFICIENCY.value: 'Эффективность',
    DatabaseField.WEEKEND.value: 'Количество выходных',
    DatabaseField.POSSIBLE_WEEKEND.value: 'Возможные выходные дни недели',
    DatabaseField.PRIORITY.value: 'Приоритет'
}
