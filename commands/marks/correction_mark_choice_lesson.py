from typing import Text
from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from ns import getSubjectsId
from PostgreSQLighter import db


bp = Blueprint('correction_mark_choice_lesson') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_lesson')
    user_id = message.from_id # ID юзера

    keyboard = Keyboard()
    lessons = await getSubjectsId( # Получаем уроки
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )

    counter = 1
    for i in lessons.keys(): # Перебираем уроки
        if counter == 4: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[:40], {"cmd": f"correction_choice_mark_{lessons[i]}"}))
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

    keyboard = Keyboard()
    lessons = await getSubjectsId( # Получаем уроки
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    counter = 1
    for i in lessons.keys(): # Перебираем уроки
        if counter == 4: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[:40], {"cmd": f"correction_choice_mark_{lessons[i]}"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text('Назад', {"cmd": "marks"}), KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔Какой предмет хотите исправить?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_lesson')