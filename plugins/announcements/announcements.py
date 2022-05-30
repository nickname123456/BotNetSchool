from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
from netschoolapi import NetSchoolAPI
import re
import logging
import os
from vkbottle import DocMessagesUploader


bp = Blueprint('announcements') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(text=["Объявления <amount>", "Объявления"])
@bp.on.private_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id
    logging.info(f'{message.peer_id}: I get "announcements {amount}"')

    try:
        # Логинимся в сго
        api = NetSchoolAPI(db.get_account_link(user_id))
        await api.login(
            db.get_account_login(user_id),
            db.get_account_password(user_id),
            db.get_account_school(user_id))
        logging.info(f'{message.peer_id}: Login in NetSchool')
        # Копируем объявления из сго
        announcements = await api.announcements()

        # Берем только те объявления, которые нужны
        announcements = announcements[:int(amount)]

        # Если есть объявления:
        if announcements:
            # Приводим объявления в нужный вид
            announcement = ''
            for i in announcements:
                announcement = "Дата: " + i['postDate'] +"\n"+ i['name'] + ":" + i['description']

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
    except: # если произошла ошибка
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        await api.logout()
        return
















@bp.on.chat_message(text=["Объявления <amount>", "Объявления"])
@bp.on.chat_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    # Айди чата:
    chat_id = message.chat_id
    logging.info(f'{message.peer_id}: I get "announcements {amount}"')

    try:
        # Логинимся в сго
        api = NetSchoolAPI(db.get_chat_link(chat_id))
        await api.login(
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id))
        logging.info(f'{message.peer_id}: Login in NetSchool')
        # Копируем объявления из сго
        announcements = await api.announcements()

        # Берем только те объявления, которые нужны
        announcements = announcements[:int(amount)]

        # Если есть объявления:
        if announcements:
            # Приводим объявления в нужный вид
            announcement = ''
            for i in announcements:
                announcement = "Дата: " + i['postDate'] +"\n"+ i['name'] + ":" + i['description']

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
    except: # если произошла ошибка
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        await api.logout()
        return