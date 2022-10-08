from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import kb_menu

import logging


async def private_menu(message: Message):
    if  isinstance(message, CallbackQuery):
        message = message.message

    user_id = message.from_user.id
    bot = message.bot

    keyboard = kb_menu
    
    #Ответ в чат
    await bot.send_message(user_id, 'Вы в главном меню.', reply_markup=keyboard)
    logging.info(f'{user_id}: I sent menu')

async def chat_menu(message: Message):
    if isinstance(message, CallbackQuery):
        message = message.message

    chat_id = message.chat.id
    bot = message.bot

    keyboard = kb_menu
    
    #Ответ в чат
    await bot.send_message(chat_id, 'Вы в главном меню.', reply_markup=keyboard)
    logging.info(f'{chat_id}: I sent menu')


def register_user_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(private_menu, lambda c: c.data and c.data =='main_menu', chat_type='private')
    dp.register_message_handler(private_menu, content_types=['text'], text=['Меню', 'меню', 'гм', 'Vty.', 'vty.', 'uv'], chat_type='private')
    
    dp.register_callback_query_handler(chat_menu, lambda c: c.data and c.data =='main_menu', chat_type='group')
    dp.register_message_handler(chat_menu, chat_type='group', content_types=['text'], text=['Меню', 'меню', 'гм', 'Vty.', 'vty.', 'uv'])