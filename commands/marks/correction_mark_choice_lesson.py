from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
from ns import get_marks

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('correction_mark_choice_lesson') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_lesson')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    keyboard = Keyboard()
    lessons = await get_marks( # Получаем уроки
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        onlySubjects= True
    )

    counter = 0
    for i in lessons: # Перебираем уроки
        if counter % 4 == 0: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
        keyboard.add(Text(i[:40], {"cmd": f"correction_choice_mark_{counter}"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text('Назад', {"cmd": "marks"}), KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔Какой предмет хотите исправить?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_lesson')




@bp.on.chat_message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_lesson')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    keyboard = Keyboard()
    lessons = await get_marks( # Получаем уроки
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId,
        onlySubjects= True
    )

    counter = 0
    for i in lessons: # Перебираем уроки
        if counter % 4 == 0: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
        keyboard.add(Text(i[:40], {"cmd": f"correction_choice_mark_{counter}"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text('Назад', {"cmd": "marks"}), KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔Какой предмет хотите исправить?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_lesson')