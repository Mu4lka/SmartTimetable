from database.enums import DatabaseField

DAY_START = 0
DAY_END = 24
MIN_SHIFT_DURATION = 1
MAX_SHIFT_DURATION = 14
KEY_LENGTH = 12

MIN_NUMBER_HOURS = 0
MAX_NUMBER_HOURS = 98

START_BOT = "Бот запущен"
SELECT_COMMAND = "Выберите команду..."
CANCEL = "Отменено"

ABOUT_NOT_AUTHORIZED = "Введите ключ для авторизации вашего аккаунта"

ENTER_FULL_NAME = ("Создание сотрудника...\nВведите полное имя (ИФ)...\n\n"
                   "Важно!!! Полное имя (ИФ) должно совпадать с расписанием")
ENTER_NUMBER_HOURS = "Введите недельную норму часов"
ENTER_USER_NAME = (f"(Не обязательно)\nВведите пользовательское имя...\n"
                   f"Например: имя_пользователя, @имя_пользователя или https://t.me/имя_пользователя")
ABOUT_CREATING_WORKER = "Вы создали сотрудника! Его параметры:\n\n"
ABOUT_SENDING_KEY_TO_WORKER = ("\nP.S. Вы можете отправить ключ сотруднику для его авторизации, "
                               "если вы не указали пользовательское имя сотрудника")

INVALID_NUMBER_HOURS = (f"Число вне диапазона!\n"
                        f"Число должно входить в диапазон от {MIN_NUMBER_HOURS} до {MAX_NUMBER_HOURS}.\n\n"
                        f"Попробуйте ещё раз...")

INVALID_INPUT = "Неверный формат ввода, попробуйте ещё раз..."
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

descriptions_worker_parameters = {
    DatabaseField.FULL_NAME.value: 'Имя',
    DatabaseField.USER_NAME.value: 'Пользовательское имя',
    DatabaseField.ID_TELEGRAM.value: 'Айди пользователя',
    DatabaseField.KEY.value: 'Ключ',
    DatabaseField.NUMBER_HOURS.value: 'Количество часов'
}
