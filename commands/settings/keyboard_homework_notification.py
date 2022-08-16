from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from commands.settings.keyboard_settings import keyboard_settings_chat, keyboard_settings_private
import logging


bp = Blueprint('keyboard_homework_notification')# Объявляем команду



@bp.on.private_message(payload={'cmd': 'keyboard_homework_notification'})
async def private_keyboard_homework_notification(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework_notification')
    user_id = message.from_id # ID юзера

    if db.get_account_homework_notification(user_id): # Если человек подписан, то отписываем его
        db.edit_account_homework_notification(user_id, 0)
        db.commit()
        await message.answer('❌Теперь вы не будете получать уведомления о новом д/з.')
    else: # Если человек не подписан, то подписываем
        db.edit_account_homework_notification(user_id, 1)
        db.commit()
        await message.answer('✅Теперь вы будете получать уведомления о новом д/з.')

    await keyboard_settings_private(message)


@bp.on.chat_message(payload={'cmd': 'keyboard_homework_notification'})
async def chat_keyboard_homeworks_notification(message: Message):
    logging.info('I get keyboard_homework_notification')
    # Айди чата:
    chat_id = message.chat_id

    if db.get_chat_homework_notification(chat_id): # Если человек подписан, то отписываем его
        db.edit_chat_homework_notification(chat_id, 0)
        db.commit()
        await message.answer('❌Теперь вы не будете получать уведомления о новом д/з.')
    else: # Если человек не подписан, то подписываем
        db.edit_chat_homework_notification(chat_id, 1)
        db.commit()
        await message.answer('✅Теперь вы будете получать уведомления о новом д/з.')

    await keyboard_settings_chat(message)