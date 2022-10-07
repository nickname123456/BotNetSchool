from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



kb_menu = InlineKeyboardMarkup(resize_keyboard=True)
kb_menu.add(InlineKeyboardButton('📢Объявления', callback_data='announcements'))
kb_menu.add(InlineKeyboardButton('📖Дневник', callback_data='keyboard_diary'),
            InlineKeyboardButton('📄Отчеты', callback_data='reports'))
kb_menu.add(InlineKeyboardButton('🏠Домашнее задание', callback_data='keyboard_homework'),
            InlineKeyboardButton('📚Расписание', callback_data='keyboard_schedule'))