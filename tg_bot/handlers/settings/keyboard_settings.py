from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from database.methods.get import get_chat_by_telegram_id, get_student_by_telegram_id
from tg_bot.keyboards import get_settings_kb

import logging


async def keyboard_settings_private(message: Message):
    if  isinstance(message, CallbackQuery):
        message = message.message
    logging.info(f'{message.chat.id}: I get settings command')

    kb = get_settings_kb(
        get_student_by_telegram_id(message.chat.id)
    )
    
    await message.answer('🤔Что хотите изменить?', reply_markup=kb)
    logging.info(f'{message.chat.id}: I send settings keyboard')


async def keyboard_settings_chat(message: Message):
    if isinstance(message, CallbackQuery):
        message = message.message
    logging.info(f'{message.chat.id}: I get settings command')

    kb = get_settings_kb(
        get_chat_by_telegram_id(message.chat.id)
    )
    
    await message.answer('🤔Что хотите изменить?', reply_markup=kb)
    logging.info(f'{message.chat.id}: I send settings keyboard')


def register_keyboard_settings_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(keyboard_settings_private, lambda c: c.data and c.data =='settings', chat_type='private')
    dp.register_message_handler(keyboard_settings_private, content_types=['text'], text=['Настройки', 'настройки', 'settings', 'Settings', '⚙Настройки'], chat_type='private')
    dp.register_message_handler(keyboard_settings_private, commands=['settings'], chat_type='private')

    dp.register_callback_query_handler(keyboard_settings_chat, lambda c: c.data and c.data =='settings', chat_type='group')
    dp.register_message_handler(keyboard_settings_chat, chat_type='group', content_types=['text'], text=['Настройки', 'настройки', 'settings', 'Settings', '⚙Настройки'])
    dp.register_message_handler(keyboard_settings_chat, chat_type='group', commands=['settings'])