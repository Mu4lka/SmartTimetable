from enums.database_field import DatabaseField
from enums.other_button import OtherButton

DAY_START = 0
DAY_END = 24
MIN_SHIFT_DURATION = 1
MAX_SHIFT_DURATION = 14
KEY_LENGTH = 12

START_BOT = "Бот запущен"
SELECT_COMMAND = "Выберите команду..."
CANCEL = "Отменено"

ABOUT_NOT_AUTHORIZED = "Введите ключ для авторизации вашего аккаунта"

ENTER_NAME = ("Создание сотрудника...\nВведите полное имя (ИФ)...\n\n"
              "Важно!!! Полное имя (ИФ) должно совпадать с расписанием")
SELECT_CREATION_TYPE = (
    "Выберите каким образом хотите создать сотрудника...\n\n"
    f"Если это \"{OtherButton.QUICKLY_CREATE.value}\", то параметры автоматически подставятся\n\n"
    f"Если это \"{OtherButton.CREATE_MANUALLY.value}\", то в ручную прописываете параметры поэтапно"
)
ENTER_SHIFT_DURATION = "Введите количество часов в смене"
ENTER_EARLY_SHIFT_START = "Введите раннее начало смены"
ENTER_LATE_SHIFT_START = "Введите позднее начало смены"
ENTER_PRIORITY = "Введите приоритет (порядковый номер для генерации расписания по убыванию)... По умолчанию 0..."
SELECT_EFFICIENCY = "Выберите эффективность"
SELECT_WEEKEND = ("Выберите первые возможные выходные дни недели и нажмите далее, чтобы дополнить этот список."
                  "Количество первых возможных выходных дней недели - это количество выходных")
SELECT_POSSIBLE_WEEKEND = "Выберите возможные выходные дни недели"
ABOUT_CREATING_WORKER = "Вы создали сотрудника! Его параметры:\n\n"
ABOUT_SENDING_KEY_TO_WORKER = "\nP.S. Отправьте ключ сотруднику, для его авторизации"

INVALID_INPUT = "Неверный формат ввода, попробуйте ещё раз..."
INVALID_SHIFT_LENGTH = (
    f"Недопустимая продолжительность смены...\n"
    f"Значение должно быть от {MIN_SHIFT_DURATION} до {MAX_SHIFT_DURATION} часов.\n\nВведите еще раз..."
)
INVALID_EARLY_SHIFT_START = ("Недопустимое раннее начало смены...\n"
                             f"Значение должно быть больше {DAY_START} и меньше {DAY_END} часов.\n\nВведите еще раз...")
INVALID_LATE_START_SHIFT = (
    "Недопустимое позднее начало смены...\n"
    f"Должно быть больше начало ранней смены и меньше {DAY_END} часов.\n\nВведите еще раз..."
)
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
