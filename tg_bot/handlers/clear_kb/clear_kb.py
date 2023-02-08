from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher

import logging


async def clear_kb(message: Message):
    logging.info(f'{message.from_user.id}: I get clear_kb')
    await message.answer('✅Клавиатура спрятана!', reply_markup=ReplyKeyboardRemove())
    logging.info(f'{message.from_user.id}: I sent clear_kb')

    


def register_clear_kb_handlers(dp: Dispatcher):
    dp.register_message_handler(clear_kb, content_types=['text'], text=['убери', 'спрячь', '/clear'])
    dp.register_message_handler(clear_kb, commands=['clear'])