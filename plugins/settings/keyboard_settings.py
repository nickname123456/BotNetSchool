from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter



bp = Blueprint('keyboard_settings')# Объявляем команду
db = SQLighter('database.db') # Подключаемся к базеданных



@bp.on.private_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_private(message: Message):
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    keyboard = Keyboard()

    if db.get_account_mark_notification(user_id):
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {"cmd": "keyboard_mark_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_account_announcements_notification(user_id):
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {"cmd": "keyboard_announcements_notification"}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('Что хочешь изменить?', keyboard=keyboard)











@bp.on.chat_message(payload={'cmd': 'keyboard_settings'})
async def keyboard_settings_chat(message: Message):
    # Айди чата:
    chat_id = message.chat_id

    keyboard = Keyboard()

    if db.get_chat_mark_notification(chat_id):
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых оценках', {'cmd': 'keyboard_mark_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()

    if db.get_chat_announcements_notification(chat_id):
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.POSITIVE)
    else:
        keyboard.add(Text('Уведомления о новых объявлениях', {'cmd': 'keyboard_announcements_notification'}), color=KeyboardButtonColor.NEGATIVE)
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.SECONDARY)

    await message.answer('Что хочешь изменить?', keyboard=keyboard)
