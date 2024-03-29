from database.methods.get import get_chats_with_homework_notification, get_homework, get_student_by_telegram_id, get_students_with_homework_notification
from database.methods.update import edit_homework, edit_homework_upd_date, edit_student_vk_id, edit_student_telegram_id
from database.methods.create import create_homework
from database.methods.delete import delete_chat
from netschoolapi import netschoolapi

from tg_bot.handlers.homework.keyboard_homework import private_keyboard_homework
from tg_bot.keyboards.inline import get_update_homework_kb, kb_back_to_homework
from tg_bot.states import HomeworkStates
from vk_bot.utils import send_vk_msg
from settings import vk_token
import ns

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
import aiogram

from vkbottle import VKAPIError
from vkbottle import Bot

from datetime import datetime
import asyncio
import logging


vk_bot = Bot(token=vk_token)

async def private_keyboard_update_homework(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get keyboard update homework')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)

    await HomeworkStates.INLESSON.set()

    try:
        kb = get_update_homework_kb(await ns.getSubjectsId(
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
    await message.edit_text('🤔На какой урок хотите изменить дз?')
    await message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{message.chat.id}: send keyboard')


async def chat_keyboard_update_homework(message: Message):
    await message.answer('❌Доступно только в л/с!')


async def get_new_homework(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f'{callback_query.message.chat.id}: get lesson for upadte homework')
    await state.update_data(lesson=callback_query.data[16:])
    await HomeworkStates.next()

    await callback_query.message.answer('📝Введите новое задание', reply_markup=kb_back_to_homework)
    logging.info(f'{callback_query.message.chat.id}: send question about new homework') 


async def private_edit_hamework(message: Message, state: FSMContext):
    logging.info(f'{message.chat.id}: get new homework')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)
    data = await state.get_data()
    lessonId = data['lesson']
    homework = message.text
    upd_date = f'{datetime.now().hour}:{datetime.now().minute} {datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
    await state.finish()

    try:
        lessons = await ns.getSubjectsId(
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId
        )
        lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]

        if get_homework(lesson, student.school, student.clas):
            edit_homework(lesson, student.school, student.clas, homework)
            edit_homework_upd_date(lesson, student.school, student.clas, upd_date)
        else:
            create_homework(lesson, student.school, student.clas, homework, upd_date)
        
        await message.answer('✅Домашнее задание успешно изменено!')
        await private_keyboard_homework(message)
        logging.info(f'{message.chat.id}: send message about success update homework')

    except TypeError:
        logging.info(f'{message.chat.id}: user not found')
        await message.answer('❌Вы не зарегистрированы! \n🤔Напишите "Начать"')
    except Exception as e:
        logging.error(f'{message.chat.id}: error: {e}')
        await message.answer(f'❌Произошла ошибка❌\n{e} \n❌Сообщите администратору❌')
    
    logging.info(f'{message.chat.id}: start mailing for users')
    users_with_notification = get_students_with_homework_notification()
    chats_with_notification = get_chats_with_homework_notification()
    for i in users_with_notification:
        telegram_id = i.telegram_id
        vk_id = i.vk_id
        if i.school == student.school: # Если школа совпадает
            if i.clas == student.clas: # Если класс совпадает
                if vk_id: # Если есть аккаунт вк
                    try: # Отправляем уведомление
                        await send_vk_msg(bot=vk_bot, user_id=vk_id, message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                        logging.info(f'{vk_id}: send vk notification')
                    except: # Если не получилось отправить
                        logging.info(f'I cannot send homework to vk user. Id: {i.vk_id}')
                if telegram_id: # Если есть аккаунт телеграм
                    try: # Отправляем уведомление
                        await message.bot.send_message(telegram_id, f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                        logging.info(f'{telegram_id}: send telegram notification')
                    except: # Если не получилось отправить
                        logging.info(f'I cannot send homework to telegram user. Id: {i.telegram_id}')
                await asyncio.sleep(1) # Отдыхаем, чтобы не спамить

    logging.info(f'{message.chat.id}: start mailing for chats')
    for i in chats_with_notification:
        telegram_id = i.telegram_id
        vk_id = i.vk_id
        if i.school == student.school:  # Если школа совпадает
            if i.clas == student.clas: # Если класс совпадает
                if vk_id: # Если есть аккаунт вк
                    try: # отправляем уведомление
                        await send_vk_msg(bot=vk_bot, chat_id=vk_id, message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                        logging.info(f'{telegram_id}: send vk notification')
                    except: # Если не получилось отправить
                        logging.info(f'I cannot send homework to vk chat. Id: {i.vk_id}')
                if telegram_id: # Если есть аккаунт телеграм
                    try: # Отправляем уведомление
                        await message.bot.send_message(telegram_id, f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                        logging.info(f'{telegram_id}: send telegram notification')
                    except: # Если не получилось отправить
                        logging.info(f'I cannot send homework to tg chat. Id: {i.telegram_id}')
                await asyncio.sleep(1) # Отдыхаем, чтобы не спамить
    logging.info(f'{message.chat.id}: end mailing')



def register_update_homework_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(chat_keyboard_update_homework, lambda c: c.data and c.data == 'update_homework', state='*', chat_type=['group', 'supergroup'])
    
    dp.register_callback_query_handler(private_keyboard_update_homework, lambda c: c.data and c.data == 'update_homework', state='*', chat_type='private')
    dp.register_callback_query_handler(get_new_homework, lambda c: c.data and c.data.startswith('update_homework_'), state=HomeworkStates.INLESSON)
    dp.register_message_handler(private_edit_hamework, state=HomeworkStates.INHOMEWORK)