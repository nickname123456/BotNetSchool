from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_marks


bp = Blueprint('marks') # Объявляем команду
db = SQLighter('database.db')# Подключаемся к базеданных


@bp.on.message(payload={'cmd': 'marks'})
@bp.on.message(text = 'оценки')
async def marks(message: Message):
    print(await get_marks('мТаскаеваЕ1Е', '123456789', 'МАОУ "СОШ № 47 г. Челябинска"', 'https://sgo.edu-74.ru'))
