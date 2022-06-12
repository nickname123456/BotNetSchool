from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
import logging
from PostgreSQLighter import db


bp = Blueprint('keyboard_homework')# Объявляем команду




@bp.on.private_message(payload={'cmd': 'keyboard_homework'})
async def private_keyboard_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework')
    userInfo = await bp.api.users.get(message.from_id)
    userId = userInfo[0].id
    
    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = db.get_lessons_with_homework(
        db.get_account_school(userId),
        db.get_account_class(userId)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "homework"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('На какой урок хочешь узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework')


@bp.on.chat_message(payload={'cmd': 'keyboard_homework'})
async def chat_keyboard_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework')
    chat_id = message.chat_id
    
    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = db.get_lessons_with_homework(
        db.get_chat_school(chat_id),
        db.get_chat_class(chat_id)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "homework"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('На какой урок хочешь узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework')