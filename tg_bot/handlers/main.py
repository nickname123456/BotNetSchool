from aiogram import Dispatcher

from tg_bot.handlers.start import register_user_start_handlers
from tg_bot.handlers.menu import register_user_menu_handlers
from tg_bot.handlers.get_connect_code import register_user_connect_code_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_start_handlers,
        register_user_menu_handlers,
        register_user_connect_code_handlers,
    )
    for handler in handlers:
        handler(dp)
