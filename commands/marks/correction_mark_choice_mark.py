from typing import Text
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from VKRules import PayloadStarts


bp = Blueprint('correction_mark_choice_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"correction_choice_mark_')
async def private_correction_mark_choice_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_mark')
    user_id = message.from_id # ID юзера

    lesson = message.payload[31:-2] # Получаем нужный урок

    db.edit_account_correction_lesson(user_id, lesson) # Изменяем урок в бд
    db.commit()

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('5️⃣', {"cmd": "correction_mark"}))
        .add(Text('4️⃣', {"cmd": "correction_mark"}))
        .add(Text('3️⃣', {"cmd": "correction_mark"}))
        .row()
        .add(Text("Назад", {'cmd': 'marks'}), color=KeyboardButtonColor.NEGATIVE)
    )
    
    logging.info(f'{message.peer_id}: I sent correction_mark_choice_mark')
    await message.answer('Какую оценку хочешь?', keyboard=keyboard)











@bp.on.chat_message(PayloadStarts='{"cmd":"correction_choice_mark_')
async def chat_correction_mark_choice_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_mark')
    # Айди чата:
    chat_id = message.chat_id
    
    lesson = message.payload[31:-2] # Получаем нужный урок

    db.edit_chat_correction_lesson(chat_id, lesson) # Изменяем урок
    db.commit()

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('5️⃣', {"cmd": "correction_mark"}))
        .add(Text('4️⃣', {"cmd": "correction_mark"}))
        .add(Text('3️⃣', {"cmd": "correction_mark"}))
        .row()
        .add(Text("Назад", {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.NEGATIVE)
    )

    logging.info(f'{message.peer_id}: I sent correction_mark_choice_mark')
    await message.answer('Какую оценку хочешь?', keyboard=keyboard)
