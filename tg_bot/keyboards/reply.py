from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_menu_kb(name) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(KeyboardButton('Войти'))
    keyboard.add(KeyboardButton('Дневник'), KeyboardButton('Домашнее задание'))
    keyboard.add(KeyboardButton('📚Расписание'), KeyboardButton('📢Объявления'),KeyboardButton('📝Отчеты'))
    keyboard.add(KeyboardButton('🔁'), KeyboardButton(name), KeyboardButton('⚙'))
    return keyboard