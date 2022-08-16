from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging


bp = Blueprint('schedule_for_day') # Объявляем команду



@bp.on.private_message(payload={'cmd': 'schedule_for_day'})
async def private_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    user_id = message.from_id # ID юзера

    try:
        if db.get_schedule(db.get_account_school(user_id),db.get_account_class(user_id), message.text)[0] is not None:
            await message.answer(attachment=db.get_schedule(db.get_account_school(user_id), db.get_account_class(user_id), message.text))
        else:
            await message.answer('❌На этот день еще нет расписания')
    except:
        await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')



@bp.on.chat_message(payload={'cmd': 'schedule_for_day'})
async def chat_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    chat_id = message.chat_id

    try:
        if db.get_schedule(db.get_chat_school(chat_id),db.get_chat_class(chat_id),message.text)[0] is not None:
            await message.answer(attachment=db.get_schedule(db.get_chat_school(chat_id), db.get_chat_class(chat_id), message.text))
        else:
            await message.answer('❌На этот день еще нет расписания')
    except:
            await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
