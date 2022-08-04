from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from ns import get_marks
from PostgreSQLighter import db


bp = Blueprint('correction_mark_choice_lesson') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_lesson')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    keyboard = Keyboard()
    lessons = await get_marks(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id),
        'all')

    counter = 1
    for i in lessons.keys():
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i, {"cmd": "correction_mark_choice_mark"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text('Назад', {"cmd": "marks"}), KeyboardButtonColor.NEGATIVE)

    await message.answer('Какой предмет хочешь исправить?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_lesson')




@bp.on.chat_message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_lesson')
    # Айди чата:
    chat_id = message.chat_id

    keyboard = Keyboard()
    lessons = await get_marks(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id),
        'all')

    counter = 1
    for i in lessons.keys():
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i, {"cmd": "correction_mark_choice_mark"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text('Назад', {"cmd": "marks"}), KeyboardButtonColor.NEGATIVE)

    await message.answer('Какой предмет хочешь исправить?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_lesson')