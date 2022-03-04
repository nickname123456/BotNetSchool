from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
import logging


bp = Blueprint('schedule_download') # Объявляем команду
db = SQLighter('database.db') # Подключаемся к базе данных



@bp.on.message(payload={'cmd': 'schedule_for_day'})
async def schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    
    # Если юзер выбрал понедельник, и на этот день есть расписание
    if 'Понедельник' in message.text and db.get_schedule(0) is not None:
        await message.answer(attachment=db.get_schedule(0))

    # Если юзер выбрал вторник, и на этот день есть расписание
    elif 'Вторник' in message.text and db.get_schedule(1) is not None:
        await message.answer(attachment=db.get_schedule(1))

    # Если юзер выбрал среду, и на этот день есть расписание
    elif 'Среда' in message.text and db.get_schedule(2) is not None:
        await message.answer(attachment=db.get_schedule(2))

    # Если юзер выбрал четверг, и на этот день есть расписание
    elif 'Четверг' in message.text and db.get_schedule(3) is not None:
        await message.answer(attachment=db.get_schedule(3))

    # Если юзер выбрал пятницу, и на этот день есть расписание
    elif 'Пятница' in message.text and db.get_schedule(4) is not None:
        await message.answer(attachment=db.get_schedule(4))
    
    else:
        await message.answer('На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
