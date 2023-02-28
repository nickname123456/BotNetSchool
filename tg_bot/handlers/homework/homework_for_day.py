from database.methods.get import get_chat_by_telegram_id, get_homework, get_student_by_telegram_id
from tg_bot.keyboards import get_homework_for_day_kb
import netschoolapi
import ns

from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

import logging

async def private_keyboard_homework_for_day(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get keyboard homework for day')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)
    week = ns.get_week()

    try:
        # Получаем дневник
        diary = await ns.get_diary(
            student.login,
            student.password,
            week,
            student.school,
            student.link,
            student.studentId
        )
        logging.info(f'{message.chat.id}: login in netschool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неверный логин или пароль')
        logging.info(f'{message.chat.id}: wrong login or password')
        return

    kb = get_homework_for_day_kb(diary, week)
    await message.answer('🤔На какой день хотите узнать домашнее задание?', reply_markup=kb)
    logging.info(f'{message.chat.id}: send keyboard homework for day')

async def chat_keyboard_homework_for_day(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get keyboard homework for day')
    chatId = message.chat.id
    chat = get_chat_by_telegram_id(chatId)
    week = ns.get_week()

    try:
        # Получаем дневник
        diary = await ns.get_diary(
            chat.login,
            chat.password,
            week,
            chat.school,
            chat.link,
            chat.studentId
        )
        logging.info(f'{message.chat.id}: login in netschool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неверный логин или пароль')
        logging.info(f'{message.chat.id}: wrong login or password')
        return

    kb = get_homework_for_day_kb(diary, week)
    await message.answer('🤔На какой день хотите узнать домашнее задание?', reply_markup=kb)
    logging.info(f'{message.chat.id}: send keyboard homework for day')


async def private_homework_for_day(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get homework for day with day')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)
    week = ns.get_week()
    day = int(callback.data.split('_')[3])

    try:
        # Получаем дневник
        diary = await ns.get_diary(
            student.login,
            student.password,
            week,
            student.school,
            student.link,
            student.studentId
        )
        logging.info(f'{message.chat.id}: login in netschool')
    except netschoolapi.errors.AuthError:
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неверный логин или пароль')
        return

    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        homework = get_homework(lesson, student.school, student.clas)
        if homework:
            await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
    logging.info(f'{message.chat.id}: send homework for day with day')

async def chat_homework_for_day(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get homework for day with day')
    chatId = message.chat.id
    chat = get_chat_by_telegram_id(chatId)
    week = ns.get_week()
    day = int(callback.data.split('_')[3])

    try:
        # Получаем дневник
        diary = await ns.get_diary(
            chat.login,
            chat.password,
            week,
            chat.school,
            chat.link,
            chat.studentId
        )
        logging.info(f'{message.chat.id}: login in netschool')
    except netschoolapi.errors.AuthError:
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неверный логин или пароль')
        return

    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        homework = get_homework(lesson, chat.school, chat.clas)
        if homework:
            await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
    logging.info(f'{message.chat.id}: send homework for day with day')

def register_handlers_homework_for_day(dp: Dispatcher):
    dp.register_callback_query_handler(private_keyboard_homework_for_day, lambda callback: callback.data.startswith('keyboard_homework_for_day'), state='*', chat_type='private')
    dp.register_callback_query_handler(chat_keyboard_homework_for_day, lambda callback: callback.data.startswith('keyboard_homework_for_day'), state='*', chat_type=['group', 'supergroup'])

    dp.register_callback_query_handler(private_homework_for_day, lambda callback: callback.data.startswith('for_day_homework_'), state='*', chat_type='private')
    dp.register_callback_query_handler(chat_homework_for_day, lambda callback: callback.data.startswith('for_day_homework_'), state='*', chat_type='group')