from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import kb_menu

import logging


async def menu(message: Message , callback_query: CallbackQuery = None):
    if callback_query is not None:
        message = callback_query.message

    user_id = message.from_user.id
    bot = message.bot

    keyboard = kb_menu
    
    #Ответ в чат
    await bot.send_message(user_id, 'Вы в главном меню.', reply_markup=keyboard)
    logging.info(f'{user_id}: I sent menu')


def register_user_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(menu, lambda c: c.data and c.data =='main_menu')
    dp.register_message_handler(menu, content_types=['text'], text=['Меню', 'меню', 'гм', 'Vty.', 'vty.', 'uv'])