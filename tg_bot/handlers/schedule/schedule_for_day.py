from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher


from database.methods.get import get_chat_by_telegram_id, get_schedule, get_student_by_telegram_id
from tg_bot.utils.send_telegram_msg import send_telegram_bytes_photo
from settings import days_and_their_variations as days

from datetime import datetime
import logging


async def private_schedule_for_day(message: Message):
    if isinstance(message, CallbackQuery):
        unfinished_day = message.data.split('_')[-1]
        message = message.message
    else:
        unfinished_day = message.text.split(' ')[-1]
    logging.info(f'{message.chat.id}: i get schedule for day' )
    
    user_id = message.chat.id
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
    student = get_student_by_telegram_id(user_id)
    schedule = get_schedule(student.school, student.clas, day)

    if schedule:
        await send_telegram_bytes_photo(bot=message.bot, chat_id=user_id, photo=schedule.photo)
    else:
        await message.answer(f'❌На этот день еще нет расписания')
    logging.info(f'{message.chat.id}: i send schedule for day' )


async def chat_schedule_for_day(message: Message):
    if isinstance(message, CallbackQuery):
        unfinished_day = message.data.split('_')[-1]
        message = message.message
    else:
        unfinished_day = message.text.split(' ')[-1]
    logging.info(f'{message.chat.id}: i get schedule for day' )

    chat_id = message.chat.id
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
    chat = get_chat_by_telegram_id(chat_id)
    schedule = get_schedule(chat.school, chat.clas, day)

    if schedule:
        await send_telegram_bytes_photo(bot=message.bot, chat_id=chat_id, photo=schedule.photo)
    else:
        await message.answer(f'❌На этот день еще нет расписания')
    logging.info(f'{message.chat.id}: i send schedule for day' )




def register_schedule_for_day_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(private_schedule_for_day, lambda c: c.data and c.data.startswith('schedule_for_day_'), state='*', chat_type='private')
    dp.register_message_handler(private_schedule_for_day, content_types=['text'], text_startswith=['расписание на ', 'Расписание на ',
                                                                                                    'скиньте расписание на', 'Скиньте расписание на',
                                                                                                    'скинь расписание на', 'Скинь расписание на'], chat_type='private')
    
    dp.register_callback_query_handler(chat_schedule_for_day, lambda c: c.data and c.data.startswith('schedule_for_day_'), state='*', chat_type=['group', 'supergroup'])
    dp.register_message_handler(chat_schedule_for_day, content_types=['text'], text_startswith=['расписание на ', 'Расписание на ',
                                                                                                'скиньте расписание на', 'Скиньте расписание на',
                                                                                                'скинь расписание на', 'Скинь расписание на'], chat_type=['group', 'supergroup'])
    