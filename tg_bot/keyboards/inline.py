from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from database.models import Student
from settings import weekDays
import datetime



kb_back_to_start_from_code = InlineKeyboardMarkup(resize_keyboard=True)
kb_back_to_start_from_code.add(InlineKeyboardButton('↩️Назад', callback_data='start_back'))


kb_menu_inline = InlineKeyboardMarkup(resize_keyboard=True)
kb_menu_inline.add(InlineKeyboardButton('📖Дневник', callback_data='keyboard_diary'),
            InlineKeyboardButton('📄Отчеты', callback_data='reports'))
kb_menu_inline.add(InlineKeyboardButton('🏠Домашнее задание', callback_data='keyboard_homework'),
            InlineKeyboardButton('📚Расписание', callback_data='keyboard_schedule'))
kb_menu_inline.add(InlineKeyboardButton('📢Объявления', callback_data='announcements'),
            InlineKeyboardButton('⚙Настройки', callback_data='settings'))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_menu.add(KeyboardButton('📖Дневник'), KeyboardButton('📄Отчеты'))
kb_menu.add(KeyboardButton('🏠Домашнее задание'), KeyboardButton('📚Расписание'))
kb_menu.add(KeyboardButton('📢Объявления'), KeyboardButton('⚙Настройки'))


admin_kb = InlineKeyboardMarkup(resize_keyboard=True)
admin_kb.add(InlineKeyboardButton('📈Статистика', callback_data='admin_stats'),
            InlineKeyboardButton('📤Рассылка', callback_data='admin_mailing'),
            InlineKeyboardButton('🔎Поиск', callback_data='admin_search'))
admin_kb.add(InlineKeyboardButton('↩️Назад', callback_data='main_menu'))


kb_reports = InlineKeyboardMarkup(resize_keyboard=True)
kb_reports.add(InlineKeyboardButton('Средний балл (БЕТА)', callback_data='marks'))
kb_reports.add(InlineKeyboardButton('Итоговые отметки', callback_data='reportTotal'), InlineKeyboardButton('Средний балл', callback_data='reportAverageMark'))
kb_reports.add(InlineKeyboardButton('Информационное письмо для родителей', callback_data='parentReport'), InlineKeyboardButton('Динамика среднего балла ученика', callback_data='reportAverageMarkDyn'))
kb_reports.add(InlineKeyboardButton('Итоги успеваемости и качества знаний', callback_data='reportGrades'))
kb_reports.add(InlineKeyboardButton('↩️Назад', callback_data='main_menu'))

kb_marks = InlineKeyboardMarkup(resize_keyboard=True)
kb_marks.add(InlineKeyboardButton('Исправление оценок', callback_data='correction_mark_choice_lesson'))
kb_marks.add(InlineKeyboardButton('↩️Назад', callback_data='reports'))

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


kb_back_to_schedule = InlineKeyboardMarkup(resize_keyboard=True)
kb_back_to_schedule.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_schedule'))

kb_back_to_homework = InlineKeyboardMarkup(resize_keyboard=True)
kb_back_to_homework.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_homework'))


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
            if (datetime.datetime.strptime(day['date'], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(diary['weekStart'], '%Y-%m-%dT%H:%M:%S')).days == i:
                kb.add(InlineKeyboardButton(weekDays[i], callback_data=f'for_day_homework_{day_number}'))
        day_number += 1
    kb.add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_homework'))
    return kb

def get_settings_kb(student: Student) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    if student.mark_notification:
        kb.add(InlineKeyboardButton('🔔Уведомления об оценках', callback_data='change_mark_notification'))
    else:
        kb.add(InlineKeyboardButton('🔕Уведомления об оценках', callback_data='change_mark_notification'))

    if student.schedule_notification:
        kb.add(InlineKeyboardButton('🔔Уведомления о расписании', callback_data='change_schedule_notification'))
    else:
        kb.add(InlineKeyboardButton('🔕Уведомления о расписании', callback_data='change_schedule_notification'))

    if student.announcements_notification:
        kb.add(InlineKeyboardButton('🔔Уведомления об объявлениях', callback_data='change_announcements_notification'))
    else:
        kb.add(InlineKeyboardButton('🔕Уведомления об объявлениях', callback_data='change_announcements_notification'))

    if student.homework_notification:
        kb.add(InlineKeyboardButton('🔔Уведомления о домашнем задании', callback_data='change_homework_notification'))
    else:
        kb.add(InlineKeyboardButton('🔕Уведомления о домашнем задании', callback_data='change_homework_notification'))
    
    kb.add(InlineKeyboardButton('↩️Назад', callback_data='exit_from_settings'))
    
    return kb

def get_correction_lessons(lessons: dict) -> InlineKeyboardMarkup:
    counter = 0
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4)
    for i in lessons:
        kb.insert(InlineKeyboardButton(i[:40], callback_data=f'correction_choice_mark_{counter}'))
        counter += 1
    kb.add(InlineKeyboardButton('↩️Назад', callback_data='marks'))
    return kb

kb_choice_mark = InlineKeyboardMarkup(resize_keyboard=True)
kb_choice_mark.add(InlineKeyboardButton('5️⃣', callback_data='choice_mark_5'))
kb_choice_mark.add(InlineKeyboardButton('4️⃣', callback_data='choice_mark_4'))
kb_choice_mark.add(InlineKeyboardButton('3️⃣', callback_data='choice_mark_3'))
kb_choice_mark.add(InlineKeyboardButton('↩️Назад', callback_data='correction_mark_choice_lesson_EDIT'))