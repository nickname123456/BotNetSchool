from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging


bp = Blueprint('schedule_for_day') # Объявляем команду



@bp.on.private_message(payload={'cmd': 'schedule_for_day'})
async def private_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    userInfo = await bp.api.users.get(message.from_id)
    user_id = userInfo[0].id

    if message.text in ['Понедельник','Вторник','Среда','Четверг','Пятница']:
        if db.get_schedule(db.get_account_school(user_id),db.get_account_class(user_id), message.text)[0] is not None:
            await message.answer(attachment=db.get_schedule(db.get_account_school(user_id), db.get_account_class(user_id), message.text))
        else:
            await message.answer('На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')



@bp.on.chat_message(payload={'cmd': 'schedule_for_day'})
async def chat_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    chat_id = message.chat_id

    if message.text in ['Понедельник','Вторник','Среда','Четверг','Пятница']:
        if db.get_schedule(db.get_chat_school(chat_id),db.get_chat_class(chat_id),message.text)[0] is not None:
            await message.answer(attachment=db.get_schedule(db.get_chat_school(chat_id),db.get_chat_class(chat_id),message.text))
        else:
            await message.answer('На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
