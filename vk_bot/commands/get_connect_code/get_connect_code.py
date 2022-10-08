from vkbottle.bot import Message, Blueprint
import logging
from random import randint
from database.methods.update import edit_student_connect_code, edit_chat_connect_code
import asyncio


bp = Blueprint('connect_code') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


@bp.on.private_message(text=['/connect', '/code', '/connectcode', '/connect_code'])
async def private_connect_code(message: Message):
    logging.info(f'{message.from_id}: I get get_connect_code')
    user_id = message.from_id

    code = randint(100000, 999999)

    edit_student_connect_code(vk_id=user_id, new_connect_code=code)
    await message.answer(f'🤫Ваш код для подключения: {code} \n❗Внимание! Код действителен только в течении 5 минут!')

    await asyncio.sleep(60 * 5)

    edit_student_connect_code(vk_id=user_id, new_connect_code=None)
    logging.info(f'{user_id}: Send connect code')

@bp.on.chat_message(text=['/connect', '/code', '/connectcode', '/connect_code'])
async def chat_connect_code(message: Message):
    logging.info(f'{message.chat_id}: I get get_connect_code')
    chat_id = message.chat_id

    code = randint(100000, 999999)

    edit_chat_connect_code(vk_id=chat_id, new_connect_code=code)
    await message.answer(f'Ваш код для подключения: {code} \nВнимание! Код действителен только в течении 5 минут!')

    await asyncio.sleep(60 * 5)

    edit_chat_connect_code(vk_id=chat_id, new_connect_code=None)
    logging.info(f'{message.chat_id}: Send connect code')