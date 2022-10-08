from .commands.settings.notification import notification
from settings import vk_token
from .commands import bps
import database

from vkbottle import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging


def start_vk_bot():

    scheduler = AsyncIOScheduler()

    # Подключаемся к базе данных
    database.register_models()

    # Подключаем бота к нашему токену
    bot = Bot(token=vk_token)

    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')




    print('')
    print('-------------------------------')
    print('  Скрипт Сетевого Города в ВК запущен.')
    print('  Разработчик: Кирилл Арзамасцев ')
    print('  https://vk.com/kirillarz')
    print('-------------------------------')
    print('')

    # Загружаем команды из папки commands
    for bp in bps:
        bp.load(bot)

    # Запускаем бота
    logging.info('Bot started.')

    scheduler.start()
    scheduler.add_job(notification, "interval", minutes=10, args=(bot,))

    bot.run_forever()