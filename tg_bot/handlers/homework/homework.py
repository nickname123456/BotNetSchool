from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from database.methods.get import get_chat_by_telegram_id, get_homework, get_student_by_telegram_id
from netschoolapi import netschoolapi
from tg_bot.keyboards import get_homework_kb
import ns

import logging

async def private_homework(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get homework command')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)

    try:
        lessons = await ns.getSubjectsId(
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId)
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неверный логин или пароль')
        logging.info(f'{message.chat.id}: wrong login or password')
        return    
    lessonId = callback.data[9:]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]

    # Получаем дз
    homework = get_homework(lesson, student.school, student.clas)
    logging.info(f'{message.chat.id}: get homework for {lesson}')

    if homework:
        await message.edit_text(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
    else:
        await message.edit_text('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')
    await message.edit_reply_markup(get_homework_kb(lessons))
    logging.info(f'{message.chat.id}: send homework')


async def chat_homework(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get homework command')
    chatId = message.chat.id
    chat = get_chat_by_telegram_id(chatId)

    try:
        lessons = await ns.getSubjectsId(
            chat.login,
            chat.password,
            chat.school,
            chat.link,
            chat.studentId)
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неверный логин или пароль')
        logging.info(f'{message.chat.id}: wrong login or password')
        return    
    lessonId = callback.data[9:]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]

    # Получаем дз
    homework = get_homework(lesson, chat.school, chat.clas)
    logging.info(f'{message.chat.id}: get homework for {lesson}')

    if homework:
        await message.edit_text(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
    else:
        await message.edit_text('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')
    await message.edit_reply_markup(get_homework_kb(lessons))
    logging.info(f'{message.chat.id}: send homework')






def register_homework_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(private_homework, lambda c: c.data.startswith('homework_'), chat_type='private')
    
    dp.register_callback_query_handler(chat_homework, lambda c: c.data.startswith('homework_'), chat_type='group')