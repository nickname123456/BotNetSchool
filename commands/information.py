from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
from ns import getSettings

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('information')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр


@bp.on.private_message(text=['/z', '/я', '/профиль', '/ghjabkm', '/profile', '/i'])
@bp.on.private_message(payload={'cmd': 'information'})
async def private_information(message: Message):
    logging.info(f'{message.peer_id}: I get information')
    user_id = message.from_id # ID юзера

    student = get_student_by_vk_id(user_id)
    try:
        result= await getSettings( # Получаем приватные данные из СГО
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId,
            student.clas
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    await message.answer(result)
    logging.info(f'{message.peer_id}: I sent information')


@bp.on.chat_message(text=['/z', '/я', '/профиль', '/ghjabkm', '/profile', '/i'])
@bp.on.chat_message(payload={'cmd': 'information'})
async def chat_information(message: Message):
    logging.info(f'{message.peer_id}: I get information')
    # Айди чата:
    chat_id = message.chat_id

    chat = get_chat_by_vk_id(chat_id)
    try:
        result= await getSettings( # Получаем приватные данные СГО
            chat.login,
            chat.password,
            chat.school,
            chat.link,
            chat.studentId,
            chat.clas
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    await message.answer(result)
    logging.info(f'{message.peer_id}: I sent information')