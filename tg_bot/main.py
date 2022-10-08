from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.filters import register_all_filters
from tg_bot.handlers import register_all_handlers

from settings import tg_token
import logging


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)


def start_tg_bot():
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='logs_tg_bot.log')

    print('')
    print('-------------------------------')
    print('  Скрипт Сетевого Города в ВК запущен.')
    print('  Разработчик: Кирилл Арзамасцев ')
    print('  https://vk.com/kirillarz')
    print('-------------------------------')
    print('')

    bot = Bot(token=tg_token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
