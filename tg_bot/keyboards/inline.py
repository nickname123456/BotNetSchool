from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from settings import weekDays




kb_menu = InlineKeyboardMarkup(resize_keyboard=True)
kb_menu.add(InlineKeyboardButton('📢Объявления', callback_data='announcements'))
kb_menu.add(InlineKeyboardButton('📖Дневник', callback_data='keyboard_diary'),
            InlineKeyboardButton('📄Отчеты', callback_data='reports'))
kb_menu.add(InlineKeyboardButton('🏠Домашнее задание', callback_data='keyboard_homework'),
            InlineKeyboardButton('📚Расписание', callback_data='keyboard_schedule'))

kb_schedule = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_schedule.add(InlineKeyboardButton('Понедельник', callback_data='schedule_for_day_monday'))
kb_schedule.add(InlineKeyboardButton('Вторник', callback_data='schedule_for_day_tuesday'))
kb_schedule.add(InlineKeyboardButton('Среда', callback_data='schedule_for_day_wednesday'))
kb_schedule.add(InlineKeyboardButton('Четверг', callback_data='schedule_for_day_thursday'))
kb_schedule.add(InlineKeyboardButton('Пятница', callback_data='schedule_for_day_friday'))
kb_schedule.add(InlineKeyboardButton('Суббота', callback_data='schedule_for_day_saturday'))
kb_schedule.add(InlineKeyboardButton('🔄Обновить', callback_data='schedule_download'),
                InlineKeyboardButton('↩️Назад', callback_data='main_menu'))


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