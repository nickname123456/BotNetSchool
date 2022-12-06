from database.methods.get import get_chat_by_telegram_id, get_student_by_telegram_id
from tg_bot.keyboards import get_homework_kb
from netschoolapi import netschoolapi
import ns

from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

import logging

async def private_keyboard_homework(message: Message, callback: CallbackQuery=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get keyboard homework command')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)

    try:
        kb = get_homework_kb(await ns.getSubjectsId(
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId))
        logging.info(f'{message.chat.id}: get keyboard')
    except netschoolapi.errors.AuthError:
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неправильный логин или пароль!')
        return

    if callback:
        await message.edit_text('🤔На какой урок хотите узнать домашнее задание?')
        await message.edit_reply_markup(kb)
    else:
        await message.answer('🤔На какой урок хотите узнать домашнее задание?', reply_markup=kb)
    logging.info(f'{message.chat.id}: send homework keyboard')

async def chat_keyboard_homework(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get keyboard homework command')
    chatId = message.chat.id
    chat = get_chat_by_telegram_id(chatId)

    try:
        kb = get_homework_kb(await ns.getSubjectsId(
            chat.login,
            chat.password,
            chat.school,
            chat.link,
            chat.studentId))
        logging.info(f'{message.chat.id}: get keyboard')
    except netschoolapi.errors.AuthError:
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неправильный логин или пароль!')
        return

    if callback:
        await message.edit_text('🤔На какой урок хотите узнать домашнее задание?')
        await message.edit_reply_markup(kb)
    else:
        await message.answer('🤔На какой урок хотите узнать домашнее задание?', reply_markup=kb)
    logging.info(f'{message.chat.id}: send homework keyboard')

    



def register_keyboard_homework_handlers(dp: Dispatcher):
    dp.register_message_handler(private_keyboard_homework, commands=['homework'], state='*', chat_type='private')
    dp.register_message_handler(private_keyboard_homework, content_types=['text'], text_startswith=['дз', '/дз', 'домашка', 'домашнее задание', 'че задали?', 'что задали?', 'че по дз?', 'что по дз?', 'какое дз?', 'что по', 'че по', '🏠Домашнее задание',
                                                                                'lp', '/lp', 'ljvfirf', 'ljvfiytt pflfybt', 'че задали', 'что задали', 'че по дз', 'что по дз', 'какое дз', 'что по', 'че по'], state='*', chat_type='private')
    dp.register_callback_query_handler(private_keyboard_homework, lambda c: c.data == 'keyboard_homework', state='*', chat_type='private')


    dp.register_message_handler(chat_keyboard_homework, commands=['homework'], state='*', chat_type='group')
    dp.register_message_handler(chat_keyboard_homework, content_types=['text'], text_startswith=['дз', '/дз', 'домашка', 'домашнее задание', 'че задали?', 'что задали?', 'че по дз?', 'что по дз?', 'какое дз?', 'что по', 'че по', '🏠Домашнее задание',
                                                                                'lp', '/lp', 'ljvfirf', 'ljvfiytt pflfybt', 'че задали', 'что задали', 'че по дз', 'что по дз', 'какое дз', 'что по', 'че по'], state='*', chat_type='group')
    dp.register_callback_query_handler(chat_keyboard_homework, lambda c: c.data == 'keyboard_homework', state='*', chat_type='group')