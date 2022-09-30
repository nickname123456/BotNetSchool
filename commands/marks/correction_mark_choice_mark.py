from database.methods.update import edit_chat_correction_lesson, edit_student_correction_lesson

from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
from VKRules import PayloadStarts

import logging


bp = Blueprint('correction_mark_choice_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"correction_choice_mark_')
async def private_correction_mark_choice_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_mark')
    user_id = message.from_id # ID юзера

    lesson = message.payload[31:-2] # Получаем нужный урок

    edit_student_correction_lesson(vk_id=user_id, new_correction_lesson=lesson) # Изменяем урок в бд

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
    await message.answer('👆🏻Какую оценку хотите?', keyboard=keyboard)











@bp.on.chat_message(PayloadStarts='{"cmd":"correction_choice_mark_')
async def chat_correction_mark_choice_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark_choice_mark')
    # Айди чата:
    chat_id = message.chat_id
    
    lesson = message.payload[31:-2] # Получаем нужный урок

    edit_chat_correction_lesson(vk_id=chat_id, new_correction_lesson=lesson) # Изменяем урок

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
    await message.answer('👆🏻Какую оценку хотите?', keyboard=keyboard)
