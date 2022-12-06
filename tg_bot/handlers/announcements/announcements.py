from aiogram.types import Message, CallbackQuery
from aiogram.types import MediaGroup
from aiogram import Dispatcher

from database.methods.get import get_chat_by_telegram_id, get_student_by_telegram_id
from tg_bot.utils import send_telegram_msg, send_telegram_media_group
from netschoolapi import NetSchoolAPI

from datetime import datetime
from io import BytesIO
import asyncio
import logging
import re

async def private_announcements(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
        amount = 3
    else:
        try:
            amount = int(message.text.split(' ')[1])
        except IndexError:
            amount = 3

    logging.info(f'{message.chat.id}: get announcements command')
    userId = message.chat.id
    student = get_student_by_telegram_id(userId)

    try:
        # логинимся в сго
        api = NetSchoolAPI(student.link)
        await api.login(
            student.login, 
            student.password,
            student.school,
            student.studentId)
    except: # Если произошла ошибка
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неверный логин или пароль')
        await api.logout()
        return
    logging.info(f'{message.chat.id}: login to netschool')

    # Копируем объявления из сго
    announcements = await api.announcements()
    # Обрезаем нужное кол-во объявлений
    announcements = announcements[:int(amount)]

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        for i in announcements:
            date = datetime.strptime(i['postDate'].split(".")[0], '%Y-%m-%dT%H:%M:%S')
            date = f'{date.hour}:{date.minute} {date.day}.{date.month}.{date.year}'
            announcement = f"📅Дата: {date} \n👩‍💼Автор: {i['author']['fio']} \n🔎Тема: {i['name']} \n💬Текст: {i['description']}"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            # Отправляем объявление
            reply_to_message_id = (await send_telegram_msg(bot=message.bot, chat_id=userId, message=announcement))['message_id']
            logging.info(f'{message.chat.id}: Send announcement')

            # Перебераем прикрепленные файлы
            media = MediaGroup()
            for attachment in i['attachments']:
                file = BytesIO((await api.download_attachment_as_bytes(attachment)))
                file.name = attachment['name']
                media.attach_document(file)
                if len(media.media) == 10: # Если медиа больше 10, то отправляем их
                    await send_telegram_media_group(bot=message.bot, chat_id=userId, media=media, reply_to_message_id=reply_to_message_id)
                    media = MediaGroup() # Обнуляем медиа
                logging.info(f'{message.chat.id}: add attachment')
                await asyncio.sleep(1)
            if media.media:
                await send_telegram_media_group(bot=message.bot, chat_id=userId, media=media, reply_to_message_id=reply_to_message_id)
            await asyncio.sleep(1)

    # Если нет объявлений:
    else:
        logging.info(f'{message.chat.id}: No announcements')
        await message.answer('❌Нет объявлений!')

    await api.logout()
    logging.info(f'{message.chat.id}: Logout from NetSchool')




async def chat_announcements(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
        amount = 3
    else:
        try:
            amount = int(message.text.split(' ')[1])
        except IndexError:
            amount = 3

    logging.info(f'{message.chat.id}: get announcements command')
    chatId = message.chat.id
    chat = get_chat_by_telegram_id(chatId)

    try:
        # логинимся в сго
        api = NetSchoolAPI(chat.link)
        await api.login(
            chat.login, 
            chat.password,
            chat.school,
            chat.studentId)
    except: # Если произошла ошибка
        logging.info(f'{message.chat.id}: wrong login or password')
        await message.answer('❌Неверный логин или пароль')
        await api.logout()
        return
    logging.info(f'{message.chat.id}: login to netschool')

    # Копируем объявления из сго
    announcements = await api.announcements()
    # Обрезаем нужное кол-во объявлений
    announcements = announcements[:int(amount)]

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        for i in announcements:
            date = datetime.strptime(i['postDate'].split(".")[0], '%Y-%m-%dT%H:%M:%S')
            date = f'{date.hour}:{date.minute} {date.day}.{date.month}.{date.year}'
            announcement = f"📅Дата: {date} \n👩‍💼Автор: {i['author']['fio']} \n🔎Тема: {i['name']} \n💬Текст: {i['description']}"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            # Отправляем объявление
            reply_to_message_id = (await send_telegram_msg(bot=message.bot, chat_id=chatId, message=announcement))['message_id']
            logging.info(f'{message.chat.id}: Send announcement')

            # Перебераем прикрепленные файлы
            media = MediaGroup()
            for attachment in i['attachments']:
                file = BytesIO((await api.download_attachment_as_bytes(attachment)))
                file.name = attachment['name']
                media.attach_document(file)
                if len(media.media) == 10: # Если медиа больше 10, то отправляем их
                    await send_telegram_media_group(bot=message.bot, chat_id=chatId, media=media, reply_to_message_id=reply_to_message_id)
                    media = MediaGroup() # Обнуляем медиа
                logging.info(f'{message.chat.id}: add attachment')
                await asyncio.sleep(1)
            if media.media:
                await send_telegram_media_group(bot=message.bot, chat_id=chatId, media=media, reply_to_message_id=reply_to_message_id)
            await asyncio.sleep(1)

    # Если нет объявлений:
    else:
        logging.info(f'{message.chat.id}: No announcements')
        await message.answer('❌Нет объявлений!')

    await api.logout()
    logging.info(f'{message.chat.id}: Logout from NetSchool')



def register_announcements_handlers(dp: Dispatcher):
    dp.register_message_handler(private_announcements, commands=['announcements'], state='*', chat_type='private')
    dp.register_message_handler(private_announcements, content_types=['text'], text_startswith=['объявления', 'объявление',
                                                                                                'Объявления', 'Объявление',
                                                                                                '📢Объявления',
                                                                                                'j,]adktybz', 'j,]zdktybt'], state='*', chat_type='private')
    dp.register_callback_query_handler(private_announcements, lambda c: c.data == 'announcements', state='*', chat_type='private')

    
    dp.register_message_handler(chat_announcements, commands=['announcements'], state='*', chat_type='group')
    dp.register_message_handler(chat_announcements, content_types=['text'], text_startswith=['объявления', 'объявление',
                                                                                                'Объявления', 'Объявление',
                                                                                                '📢Объявления',
                                                                                                'j,]adktybz', 'j,]zdktybt'], state='*', chat_type='group')
    dp.register_callback_query_handler(chat_announcements, lambda c: c.data == 'announcements', state='*', chat_type='group')