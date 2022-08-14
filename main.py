from vkbottle import Bot
from commands import bps
from settings import token
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands.settings.notification import notification

scheduler = AsyncIOScheduler()

# Подключаем бота к нашему токену
bot = Bot(token=token)

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')




print('')
print('-------------------------------')
print('  Скрипт Сетевого Города запущен.')
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
scheduler.add_job(notification, "interval", minutes=60, args=(bot,))

bot.run_forever()