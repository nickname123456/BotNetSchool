from database.methods.get import get_chat_by_vk_id, get_schedule, get_student_by_vk_id
from settings import days_and_their_variations as days

from vkbottle.bot import Message, Blueprint
from vkbottle import PhotoMessageUploader

from datetime import datetime
import logging



bp = Blueprint('schedule_for_day') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр


@bp.on.private_message(text=['расписание на <unfinished_day>'])
@bp.on.private_message(payload={'cmd': 'schedule_for_day'})
async def private_schedule_for_day(message: Message, unfinished_day = None):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    user_id = message.from_id # ID юзера
    if unfinished_day:
        if unfinished_day == 'завтра':
            unfinished_day = datetime.today().weekday() + 2 # +2 потому что отчёт идёт с 0, а не с 1
        elif unfinished_day == 'сегодня':
            unfinished_day = datetime.today().weekday() + 1 # +1 потому что отчёт идёт с 0, а не с 1
        elif unfinished_day == 'вчера':
            unfinished_day = datetime.today().weekday() # +0 потому что отчёт идёт с 0, а не с 1
        day = [i for i in days if unfinished_day in days[i]][0] # Получаем день недели
    else:
        day = [i for i in days if message.text.lower() in days[i]][0] # Получаем день недели
    student = get_student_by_vk_id(user_id)
    schedule = get_schedule(student.school, student.clas, day)

    if schedule is not None:
        photo = await PhotoMessageUploader(api=message.ctx_api).upload(schedule.photo) # Загружаем фото на сервера ВК
        await message.answer(attachment=photo)
    else:
        await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')



@bp.on.chat_message(text=['расписание на <unfinished_day>'])
@bp.on.chat_message(payload={'cmd': 'schedule_for_day'})
async def private_schedule_for_day(message: Message, unfinished_day = None):
    logging.info(f'{message.peer_id}: I get schedule_for_day')
    chat_id = message.chat_id
    if unfinished_day:
        if unfinished_day == 'завтра':
            unfinished_day = datetime.today().weekday() + 2 # +2 потому что отчёт идёт с 0, а не с 1
        elif unfinished_day == 'сегодня':
            unfinished_day = datetime.today().weekday() + 1 # +1 потому что отчёт идёт с 0, а не с 1
        elif unfinished_day == 'вчера':
            unfinished_day = datetime.today().weekday() # +0 потому что отчёт идёт с 0, а не с 1
        day = [i for i in days if unfinished_day in days[i]][0] # Получаем день недели
    else:
        day = [i for i in days if message.text.lower() in days[i]][0] # Получаем день недели
    chat = get_chat_by_vk_id(chat_id)
    schedule = get_schedule(chat.school, chat.clas, day)

    if schedule is not None:
        photo = await PhotoMessageUploader(api=message.ctx_api).upload(schedule.photo) # Загружаем фото на сервера ВК
        await message.answer(attachment=photo)
    else:
        await message.answer('❌На этот день еще нет расписания')

    logging.info(f'{message.peer_id}: I sent keyboard_schedule')