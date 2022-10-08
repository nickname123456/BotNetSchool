from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging



bp = Blueprint('keyboard_settings')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр



@bp.on.message(text=['/settings', '/yfcnhjqrb', '/настройки'])
@bp.on.private_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_private(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_settings')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    keyboard = Keyboard()
    # 
    # Если человек подписан, то кнопка зеленная, в ином случае - красная
    # 
    if student.mark_notification:
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if student.schedule_notification:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if student.announcements_notification:
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if student.homework_notification:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('🤔Что хотите изменить?', keyboard=keyboard)


@bp.on.message(text=['/settings', '/yfcnhjqrb', '/настройки'])
@bp.on.chat_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_chat(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_settings')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    keyboard = Keyboard()
    # 
    # Если человек подписан, то кнопка зеленная, в ином случае - красная
    # 
    if chat.mark_notification:
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if chat.schedule_notification:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом расписании', {"cmd": "keyboard_schedule_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if chat.announcements_notification:
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if chat.homework_notification:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новом д/з', {'cmd': 'keyboard_homework_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('🤔Что хотите изменить?', keyboard=keyboard)