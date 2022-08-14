import asyncio
from typing import Text
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from ns import get_marks
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging


bp = Blueprint('marks') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'marks'})
@bp.on.private_message(text = 'оценки')
async def private_marks(message: Message):
    logging.info(f'{message.peer_id}: I get marks')
    user_id = message.from_id # ID юзера

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Исправление оценок', {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    await asyncio.sleep(1)
    await message.answer(
        await get_marks(    
            db.get_account_login(user_id),
            db.get_account_password(user_id),
            db.get_account_school(user_id),
            db.get_account_link(user_id),
            db.get_account_studentId(user_id)
        ), 
        keyboard=keyboard
    )
    logging.info(f'{message.peer_id}: I sent marks')



@bp.on.chat_message(payload={'cmd': 'marks'})
@bp.on.chat_message(text = 'оценки')
async def chat_marks(message: Message):
    logging.info(f'{message.peer_id}: I get marks')
    # Айди чата:
    chat_id = message.chat_id

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Исправление оценок', {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)
    )

    
    await message.answer('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    await message.answer(
        await get_marks(    
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_studentId(chat_id)
        ), 
        keyboard=keyboard
    )
    logging.info(f'{message.peer_id}: I sent marks')