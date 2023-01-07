from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from database.methods.get import get_chat_by_telegram_id, get_student_by_telegram_id

from tg_bot.keyboards import kb_marks
from ns import get_marks

import logging

async def private_marks(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get private_marks command')

    user_id = message.chat.id
    student = get_student_by_telegram_id(user_id)
    if callback:
        await message.edit_text('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    else:
        await message.answer('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    await message.answer(
        await get_marks(
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId
        ), 
        reply_markup=kb_marks
    )

    logging.info(f'{message.chat.id}: I sent private_marks')


async def chat_marks(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get private_marks command')

    chat_id = message.chat.id
    chat = get_chat_by_telegram_id(chat_id)

    if callback:
        await message.edit_text('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    else:
        await message.answer('⚠Внимание! Это не официальный отчет СГО. Оценки берутся путем "перелистывания" всего Дневника. Из-за этого могут быть ошибки. \n❗НО плюсы этого отчета в том, что можно посмотреть как можно исправить текущие оценки!')
    await message.answer(
        await get_marks(
            chat.login,
            chat.password,
            chat.school,
            chat.link,
            chat.studentId
        ), 
reply_markup=kb_marks
    )

    logging.info(f'{message.chat.id}: I sent private_marks')

def register_handlers_marks(dp: Dispatcher):
    dp.register_message_handler(private_marks, commands=['marks'], state='*', chat_type='private')
    dp.register_message_handler(private_marks, content_types=['text'], text_startswith=['оценки', 'Оценки'], state='*', chat_type='private')
    dp.register_callback_query_handler(private_marks, lambda c: c.data == 'marks', state='*', chat_type='private')


    dp.register_message_handler(chat_marks, commands=['marks'], state='*', chat_type='group')
    dp.register_message_handler(chat_marks, content_types=['text'], text_startswith=['оценки', 'Оценки'], state='*', chat_type='group')
    dp.register_callback_query_handler(chat_marks, lambda c: c.data == 'marks', state='*', chat_type='group')