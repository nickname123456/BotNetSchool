from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from random import randint
from database.methods.update import edit_student_connect_code
import asyncio

import logging


async def private_connect_code(message: Message , callback_query: CallbackQuery = None):
    logging.info(f'{message.from_user.id}: I get get_connect_code')
    if callback_query is not None:
        message = callback_query.message
    user_id = message.from_user.id

    code = randint(100000, 999999)

    edit_student_connect_code(telegram_id=user_id, new_connect_code=code)
    await message.answer(f'🤫Ваш код для подключения: {code} \n❗Внимание! Код действителен только в течении 5 минут!')

    await asyncio.sleep(60 * 5)

    edit_student_connect_code(telegram_id=user_id, new_connect_code=None)
    logging.info(f'{user_id}: Send connect code')


def register_user_connect_code_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(private_connect_code, lambda c: c.data and c.data =='get_connect_code')
    dp.register_message_handler(private_connect_code, content_types=['text'], text=['/connect', '/code', '/connectcode', '/connect_code'])
    dp.register_message_handler(private_connect_code, commands=['code'])