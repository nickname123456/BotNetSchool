from vkbottle import Bot
from plugins import bps
from settings import token

# Подключаем бота к нашему токену
bot = Bot(token=token)



print('')
print('-------------------------------')
print('  Скрипт Сетевого Города запущен.')
print('  Разработчик: Кирилл Арзамасцев ')
print('  https://vk.com/kirillarz')
print('-------------------------------')
print('')

# Загружаем команды из папки plugins
for bp in bps:
    bp.load(bot)

# Запускаем бота
bot.run_forever()
