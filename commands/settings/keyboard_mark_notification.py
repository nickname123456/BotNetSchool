from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
from commands.settings.keyboard_settings import keyboard_settings_chat, keyboard_settings_private
import logging



bp = Blueprint('keyboard_mark_notification')# Объявляем команду



@bp.on.private_message(payload={'cmd': 'keyboard_mark_notification'})
async def private_keyboard_mark_notification(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_mark_notification')
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if db.get_account_mark_notification(user_id):
        db.edit_account_mark_notification(user_id, 0)
        db.commit()
        await message.answer('Теперь ты не будешь получать уведомления о новых оценках.')
    else:
        db.edit_account_mark_notification(user_id, 1)
        db.commit()
        await message.answer('Теперь ты будешь получать уведомления о новых оценках.')

    await keyboard_settings_private(message)

@bp.on.chat_message(payload={'cmd': 'keyboard_mark_notification'})
async def chat_keyboard_mark_notification(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_mark_notification')
    # Айди чата:
    chat_id = message.chat_id

    if db.get_chat_mark_notification(chat_id):
        db.edit_chat_mark_notification(chat_id, 0)
        db.commit()
        await message.answer('Теперь вы не будете получать уведомления о новых оценках.')
    else:
        db.edit_chat_mark_notification(chat_id, 1)
        db.commit()
        await message.answer('Теперь вы будете получать уведомления о новых оценках.')

    await keyboard_settings_chat(message)