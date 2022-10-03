from database.methods.update import switch_student_schedule_notification, switch_chat_schedule_notification
from vk_bot.commands.settings.keyboard_settings import keyboard_settings_chat, keyboard_settings_private
from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('keyboard_schedule_notification')# Объявляем команду



@bp.on.private_message(payload={'cmd': 'keyboard_schedule_notification'})
async def private_keyboard_schedule_notification(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_schedule_notification')
    user_id = message.from_id # ID юзера

    switch_student_schedule_notification(vk_id=user_id)

    if get_student_by_vk_id(user_id).schedule_notification:
        await message.answer('✅Теперь вы будете получать уведомления о новых объявлениях.')
    else:
        await message.answer('❌Теперь вы не будете получать уведомления о новых объявлениях.')

    await keyboard_settings_private(message)

@bp.on.chat_message(payload={'cmd': 'keyboard_schedule_notification'})
async def chat_keyboard_schedule_notification(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_schedule_notification')
    # Айди чата:
    chat_id = message.chat_id

    switch_chat_schedule_notification(vk_id=chat_id)

    if get_chat_by_vk_id(chat_id).schedule_notification:
        await message.answer('✅Теперь вы будете получать уведомления о новых объявлениях.')
    else:
        await message.answer('❌Теперь вы не будете получать уведомления о новых объявлениях.')

    await keyboard_settings_chat(message)