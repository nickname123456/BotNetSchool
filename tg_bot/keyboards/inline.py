from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from settings import weekDays




kb_menu_inline = InlineKeyboardMarkup(resize_keyboard=True)
kb_menu_inline.add(InlineKeyboardButton('📢Объявления', callback_data='announcements'))
kb_menu_inline.add(InlineKeyboardButton('📖Дневник', callback_data='keyboard_diary'),
            InlineKeyboardButton('📄Отчеты', callback_data='reports'))
kb_menu_inline.add(InlineKeyboardButton('🏠Домашнее задание', callback_data='keyboard_homework'),
            InlineKeyboardButton('📚Расписание', callback_data='keyboard_schedule'))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_menu.add(KeyboardButton('📢Объявления'))
kb_menu.add(KeyboardButton('📖Дневник'), KeyboardButton('📄Отчеты'))
kb_menu.add(KeyboardButton('🏠Домашнее задание'), KeyboardButton('📚Расписание'))


kb_schedule = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_schedule.add(InlineKeyboardButton('Понедельник', callback_data='schedule_for_day_monday'))
kb_schedule.add(InlineKeyboardButton('Вторник', callback_data='schedule_for_day_tuesday'))
kb_schedule.add(InlineKeyboardButton('Среда', callback_data='schedule_for_day_wednesday'))
kb_schedule.add(InlineKeyboardButton('Четверг', callback_data='schedule_for_day_thursday'))
kb_schedule.add(InlineKeyboardButton('Пятница', callback_data='schedule_for_day_friday'))
kb_schedule.add(InlineKeyboardButton('Суббота', callback_data='schedule_for_day_saturday'))
kb_schedule.add(InlineKeyboardButton('🔄Обновить', callback_data='schedule_download'),
                InlineKeyboardButton('↩️Назад', callback_data='main_menu'))

kb_schedule_download = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_schedule_download.add(InlineKeyboardButton('Понедельник', callback_data='update_schedule_monday'))
kb_schedule_download.add(InlineKeyboardButton('Вторник', callback_data='update_schedule_tuesday'))
kb_schedule_download.add(InlineKeyboardButton('Среда', callback_data='update_schedule_wednesday'))
kb_schedule_download.add(InlineKeyboardButton('Четверг', callback_data='update_schedule_thursday'))
kb_schedule_download.add(InlineKeyboardButton('Пятница', callback_data='update_schedule_friday'))
kb_schedule_download.add(InlineKeyboardButton('Суббота', callback_data='update_schedule_saturday'))
kb_schedule_download.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_schedule'))


def get_homework_kb(lessons: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4)
    for i in lessons:
        kb.insert(InlineKeyboardButton(i, callback_data=f'homework_{lessons[i]}'))
    kb.add(InlineKeyboardButton('📅Все дз на 1 день', callback_data='keyboard_homework_for_day'))
    kb.add(InlineKeyboardButton('🔄Обновить', callback_data='update_homework'),
        InlineKeyboardButton('↩️Назад', callback_data='main_menu'))
    return kb


def get_update_homework_kb(lessons: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4)
    for i in lessons:
        kb.insert(InlineKeyboardButton(i, callback_data=f'update_homework_{lessons[i]}'))
    kb.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_homework'))
    return kb

def get_homework_for_day_kb(diary, week) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4)
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                kb.add(InlineKeyboardButton(weekDays[i], callback_data=f'for_day_homework_{day_number}'))
        day_number += 1
    kb.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_homework'))
    return kb