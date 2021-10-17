from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from netschoolapi import NetSchoolAPI
import netschoolapi
from sqlighter import SQLighter


bp = Blueprint('schedule_download')
db = SQLighter('database.db')



@bp.on.message(payload={'cmd': 'schedule_for_day'})
async def schedule_for_day(message: Message):
    
    print(db.get_schedule(0))
    if 'Понедельник' in message.text and db.get_schedule(0) is not None:
        print(db.get_schedule(0))
        await message.answer(attachment=db.get_schedule(0))

    elif 'Вторник' in message.text and db.get_schedule(1) is not None:
        await message.answer(attachment=db.get_schedule(1))

    elif 'Среда' in message.text and db.get_schedule(2) is not None:
        await message.answer(attachment=db.get_schedule(2))

    elif 'Четверг' in message.text and db.get_schedule(3) is not None:
        await message.answer(attachment=db.get_schedule(3))

    elif 'Пятница' in message.text and db.get_schedule(4) is not None:
        await message.answer(attachment=db.get_schedule(4))
    
    else:
        await message.answer('На этот день еще нет расписания')
