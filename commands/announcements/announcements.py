from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
from netschoolapi import NetSchoolAPI

from vkbottle.bot import Message, Blueprint
from vkbottle import DocMessagesUploader

from datetime import datetime
import logging
import re


bp = Blueprint('announcements') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(text=["Объявления <amount>", "Объявления"])
@bp.on.private_message(payload={'cmd': 'announcements'})
async def private_announcements(message: Message, amount=3):
    logging.info(f'{message.peer_id}: I get "announcements {amount}"')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    try:
        # Логинимся в сго
        api = NetSchoolAPI(student.link)
        await api.login(
            student.login,
            student.password,
            student.school,
            student.studentId)
    except: # если произошла ошибка
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Ты не зарегистрирован! \n🤔Напиши "Начать"\n ❌Или у тебя неверный логин/пароль')
        await api.logout()
        return
    logging.info(f'{message.peer_id}: Login in NetSchool')

    # Копируем объявления из сго
    announcements = await api.announcements()
    # Обрезаем нужное кол-во объявлений
    announcements = announcements[:int(amount)]

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        for i in announcements:
            date = datetime.strptime(i['postDate'], '%Y-%m-%dT%H:%M:%S.%f')
            date = f'{date.hour}:{date.minute} {date.day}.{date.month}.{date.year}'
            announcement = f"📅Дата: {date} \n👩‍💼Автор: {i['author']['fio']} \n🔎Тема: {i['name']} \n💬Текст: {i['description']}"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            # Отправляем объявление
            await message.answer(announcement)
            logging.info(f'{message.peer_id}: Send announcement')

            # Перебераем прикрепленные файлы
            for attachment in i['attachments']:
                # Скачиваем файл
                file = await api.download_attachment_as_bytes(attachment)

                # Отправляем файл
                attach = await DocMessagesUploader(api=message.ctx_api).upload(file_source = file,title = attachment['name'] ,peer_id=message.peer_id)
                await message.answer(attachment=attach)
                logging.info(f'{message.peer_id}: Send attachment')

            # Делаем пробел между объявлениями
            await message.answer('&#12288;')

    # Если нет объявлений:
    else:
        logging.info(f'{message.peer_id}: No announcements')
        await message.answer('❌Нет объявлений!')

    await api.logout()
    logging.info(f'{message.peer_id}: Logout from NetSchool')



@bp.on.chat_message(text=["Объявления <amount>", "Объявления"])
@bp.on.chat_message(payload={'cmd': 'announcements'})
async def chat_announcements(message: Message, amount=3):
    logging.info(f'{message.peer_id}: I get "announcements {amount}"')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    try:
        # Логинимся в сго
        api = NetSchoolAPI(chat.link)
        await api.login(
            chat.login,
            chat.password,
            chat.school,
            chat.studentId)
    except: # если произошла ошибка
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Ты не зарегистрирован! \n🤔Напиши "Начать"\n ❌Или у тебя неверный логин/пароль')
        await api.logout()
        return
    logging.info(f'{message.peer_id}: Login in NetSchool')

    # Копируем объявления из сго
    announcements = await api.announcements()
    # Обрезаем нужное кол-во объявлений
    announcements = announcements[:int(amount)]

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        for i in announcements:
            date = datetime.strptime(i['postDate'], '%Y-%m-%dT%H:%M:%S.%f')
            date = f'{date.hour}:{date.minute} {date.day}.{date.month}.{date.year}'
            announcement = f"📅Дата: {date} \n👩‍💼Автор: {i['author']['fio']} \n🔎Тема: {i['name']} \n💬Текст: {i['description']}"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            # Отправляем объявление
            await message.answer(announcement)
            logging.info(f'{message.peer_id}: Send announcement')

            # Перебераем прикрепленные файлы
            for attachment in i['attachments']:
                # Скачиваем файл
                file = await api.download_attachment_as_bytes(attachment)

                # Отправляем файл
                attach = await DocMessagesUploader(api=message.ctx_api).upload(file_source = file,title = attachment['name'] ,peer_id=message.peer_id)
                await message.answer(attachment=attach)
                logging.info(f'{message.peer_id}: Send attachment')

            # Делаем пробел между объявлениями
            await message.answer('&#12288;')

    # Если нет объявлений:
    else:
        logging.info(f'{message.peer_id}: No announcements')
        await message.answer('❌Нет объявлений!')

    await api.logout()
    logging.info(f'{message.peer_id}: Logout from NetSchool')