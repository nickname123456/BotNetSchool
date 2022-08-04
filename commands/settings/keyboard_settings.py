from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging



bp = Blueprint('keyboard_settings')# Объявляем команду



@bp.on.private_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_private(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_settings')
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    keyboard = Keyboard()

    if db.get_account_mark_notification(user_id):
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_account_schedule_notification(user_id):
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_account_announcements_notification(user_id):
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_account_homework_notification(user_id):
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('Что хочешь изменить?', keyboard=keyboard)


@bp.on.chat_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_chat(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_settings')
    # Айди чата:
    chat_id = message.chat_id

    keyboard = Keyboard()

    if db.get_chat_mark_notification(chat_id):
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_chat_schedule_notification(chat_id):
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_chat_announcements_notification(chat_id):
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_chat_homework_notification(chat_id):
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('Что хочешь изменить?', keyboard=keyboard)
