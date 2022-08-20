from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from PostgreSQLighter import db
import ns


bp = Blueprint('keyboard_homework')# Объявляем команду




@bp.on.private_message(payload={'cmd': 'keyboard_homework'})
async def private_keyboard_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework')
    userId = message.from_id # ID юзера
    
    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = await ns.getSubjectsId(
        db.get_account_login(userId),
        db.get_account_password(userId),
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId)
    )
    counter = 1
    for i in lessons: # Перебираем уроки
        if counter == 4: # если в строке уже 4 урока, переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[:40], {"cmd": f"homework_{lessons[i]}"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой урок хотите узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework')


@bp.on.chat_message(payload={'cmd': 'keyboard_homework'})
async def chat_keyboard_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework')
    chat_id = message.chat_id
    
    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = await ns.getSubjectsId(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    counter = 1
    for i in lessons: # Перебираем уроки
        if counter == 4:  # если в строке уже 4 урока, переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[:40], {"cmd": f"homework_{lessons[i]}"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой урок хотите узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework')