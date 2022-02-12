from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_marks
from vkbottle import Keyboard, KeyboardButtonColor, Text


bp = Blueprint('marks') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений

db = SQLighter('database.db')# Подключаемся к базеданных


@bp.on.private_message(payload={'cmd': 'marks'})
@bp.on.private_message(text = 'оценки')
async def marks(message: Message):
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Исправление оценок', {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer(
        await get_marks(    
            db.get_account_login(user_id),
            db.get_account_password(user_id),
            db.get_account_school(user_id),
            db.get_account_link(user_id)
        ), 
        keyboard=keyboard
    )



@bp.on.chat_message(payload={'cmd': 'marks'})
@bp.on.chat_message(text = 'оценки')
async def marks(message: Message):
    # Айди чата:
    chat_id = message.chat_id

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Исправление оценок', {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer(
        await get_marks(    
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id)
        ), 
        keyboard=keyboard
    )