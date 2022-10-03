from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
from ns import get_marks

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('marks') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'marks'})
@bp.on.private_message(text=['оценки', 'jwtyrb', '/marks', '/оценки'])
async def private_marks(message: Message):
    logging.info(f'{message.peer_id}: I get marks')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

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
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId
        ), 
        keyboard=keyboard
    )
    logging.info(f'{message.peer_id}: I sent marks')



@bp.on.chat_message(payload={'cmd': 'marks'})
@bp.on.chat_message(text=['оценки', 'jwtyrb', '/marks', '/оценки'])
async def chat_marks(message: Message):
    logging.info(f'{message.peer_id}: I get marks')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

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
            chat.login,
            chat.password,
            chat.school,
            chat.link,
            chat.studentId
        ), 
        keyboard=keyboard
    )
    logging.info(f'{message.peer_id}: I sent marks')