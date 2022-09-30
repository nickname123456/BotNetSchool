from database.methods.get import get_chat_by_vk_id, get_schedule, get_student_by_vk_id

from vkbottle.bot import Message, Blueprint

import logging



bp = Blueprint('schedule_for_day') # Объявляем команду



@bp.on.private_message(payload={'cmd': 'schedule_for_day'})
async def private_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)
    schedule = get_schedule(student.school, student.clas, message.text)

    if schedule is not None:
        await message.answer(attachment=schedule.photo)
    else:
        await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')



@bp.on.chat_message(payload={'cmd': 'schedule_for_day'})
async def chat_schedule_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    schedule = get_schedule(chat.school, chat.clas, message.text)

    if schedule is not None:
        await message.answer(attachment=schedule.photo)
    else:
        await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
