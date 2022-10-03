from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.filters import register_all_filters
from tg_bot.handlers import register_all_handlers

from settings import tg_token


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)


def start_tg_bot():
    bot = Bot(token=tg_token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
