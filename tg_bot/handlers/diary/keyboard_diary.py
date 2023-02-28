from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

import logging


async def private_keyboard_diary(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = callback.message
    logging.info(f'{message.chat.id}: I get diary')
    await message.answer("🙄Когда-нибудь админ обязательно сделает эту функцию и в телеграме.. \n😘Но сейчас вы можети зайти в дневник через <a href='https://vk.com/botnetschool'>ВК бота</a>", disable_web_page_preview=True)
    logging.info(f'{message.chat.id}: I sent diary')


async def chat_keyboard_diary(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = callback.message
    logging.info(f'{message.chat.id}: I get diary')
    await message.answer("🙄Когда-нибудь админ обязательно сделает эту функцию и в телеграме.. \n😘Но сейчас вы можети зайти в дневник через <a href='https://vk.com/botnetschool'>ВК бота</a>", disable_web_page_preview=True)
    logging.info(f'{message.chat.id}: I sent diary')

    


def register_keyboard_diary_handlers(dp: Dispatcher):
    dp.register_message_handler(private_keyboard_diary, content_types=['text'], text=['📖Дневник', 'Дневник', 'дневник', '/diary'], state='*', chat_type='private')
    dp.register_message_handler(chat_keyboard_diary, content_types=['text'], text=['📖Дневник', 'Дневник', 'дневник', '/diary'], state='*', chat_type=['group', 'supergroup'])
    
    dp.register_callback_query_handler(private_keyboard_diary, lambda c: c.data == 'keyboard_diary', state='*', chat_type='private')
    dp.register_callback_query_handler(chat_keyboard_diary, lambda c: c.data == 'keyboard_diary', state='*', chat_type=['group', 'supergroup'])