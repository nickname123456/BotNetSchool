from vkbottle import Bot
from plugins import bps

bot = Bot(token="cbe860721ab36e8e5431d82aa7a45978bfef412294cc1bbdbd652c0f8318578ee24161ee054ad30593bbf")

print('')
print('-------------------------------')
print('  Скрипт Сетевого Города запущен.')
print('  Разработчик: Кирилл Арзамасцев ')
print('  https://vk.com/kirillarz')

print('-------------------------------')
print('')

for bp in bps:
    bp.load(bot)

bot.run_forever()
