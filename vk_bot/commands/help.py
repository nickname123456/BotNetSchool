from vkbottle.bot import Message, Blueprint
import logging


bp = Blueprint('help') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


@bp.on.message(text=['помощь', 'help', '/помощь', '/help'])
async def help(message: Message):
    logging.info(f'{message.peer_id}: I get help')

    await message.answer(
        """
😃Мои команды:
/старт - зарегистрироваться в Боте
/меню - зайти в главное меню
/дневник - зайти в дневник СГО
/дз - посмотреть домашнее задание
/расписание - посмотреть расписание
/отчеты - посмотреть отчеты
/профиль - зайти в свой профиль СГО
/настройки - изменить настройки
/репорт - сообщить об ошибке
/клавиатура - спрятать кнопки
        """)
    
    await message.answer('Более подробный разбор команд доступен по ссылке: https://vk.com/@botnetschool-kak-polzovatsya')