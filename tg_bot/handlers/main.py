from aiogram import Dispatcher

from tg_bot.handlers.start import register_user_start_handlers, register_chat_start_handlers
from tg_bot.handlers.menu import register_user_menu_handlers
from tg_bot.handlers.get_connect_code import register_user_connect_code_handlers
from tg_bot.handlers.schedule import register_schedule_handlers, register_schedule_for_day_handlers, register_schedule_download
from tg_bot.handlers.homework import register_keyboard_homework_handlers, register_homework_handlers, register_update_homework_handlers, register_handlers_homework_for_day
from tg_bot.handlers.settings import register_keyboard_settings_handlers, register_change_settings_notification_handlers, register_exit_from_settings_handlers
from tg_bot.handlers.announcements import register_announcements_handlers

def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_start_handlers,
        register_user_menu_handlers,
        register_user_connect_code_handlers,
        register_chat_start_handlers,
        register_schedule_handlers,
        register_schedule_for_day_handlers,
        register_schedule_download,
        register_keyboard_homework_handlers,
        register_homework_handlers,
        register_handlers_homework_for_day,
        register_update_homework_handlers,
        register_keyboard_settings_handlers,
        register_change_settings_notification_handlers,
        register_exit_from_settings_handlers,
        register_announcements_handlers,
    )
    for handler in handlers:
        handler(dp)
