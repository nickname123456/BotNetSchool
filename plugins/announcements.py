from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from netschoolapi import NetSchoolAPI
import re
from vkbottle import DocMessagesUploader
import os


bp = Blueprint('announcements') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений

db = SQLighter('database.db') # Подключаемся к базеданных


@bp.on.private_message(text=["Объявления <amount>", "Объявления"])
@bp.on.private_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    try:
        # Логинимся в сго
        api = NetSchoolAPI(db.get_account_link(user_id))
        await api.login(
            db.get_account_login(user_id),
            db.get_account_password(user_id),
            db.get_account_school(user_id))
        # Копируем объявления из сго
        announcements = await api.announcements()

        # Берем только те объявления, которые нужны
        announcements = announcements[:int(amount)]

        # Если есть объявления:
        if announcements:
            # Приводим объявления в нужный вид
            announcement = ''
            for i in announcements:
                announcement = f"Дата: {i.post_date.date()}\n{i.name}:\n{i.content}\n"

                announcement = re.sub(r'\<[^>]*\>', '', announcement)

                # Отправляем объявление
                await message.answer(announcement)

                # Перебераем прикрепленные файлы
                for attachment in i.attachments:
                    # Скачиваем файл
                    await api.download_attachment(attachment)
                    # Путь к файлу:
                    attachment_source = attachment.name

                    # Отправляем файл
                    attach = await DocMessagesUploader(api=message.ctx_api).upload(file_source = attachment_source,title = attachment.name ,peer_id=message.peer_id)
                    await message.answer(attachment=attach)

                    # Удаляем файл
                    os.remove(attachment_source)


                # Делаем пробел между объявлениями
                await message.answer('&#12288;')

        # Если нет объявлений:
        else:
            await message.answer('❌Нет объявлений!')


        await api.logout()
    except: # если произошла ошибка
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        await api.logout()
        return
















@bp.on.chat_message(text=["Объявления <amount>", "Объявления"])
@bp.on.chat_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    # Айди чата:
    chat_id = message.chat_id

    try:
        # Логинимся в сго
        api = NetSchoolAPI(db.get_chat_link(chat_id))
        await api.login(
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id))
        # Копируем объявления из сго
        announcements = await api.announcements()

        # Берем только те объявления, которые нужны
        announcements = announcements[:int(amount)]

        # Если есть объявления:
        if announcements:
            # Приводим объявления в нужный вид
            announcement = ''
            for i in announcements:
                announcement = f"Дата: {i.post_date.date()}\n{i.name}:\n{i.content}\n"

                announcement = re.sub(r'\<[^>]*\>', '', announcement)

                # Отправляем объявление
                await message.answer(announcement)

                # Перебераем прикрепленные файлы
                for attachment in i.attachments:
                    # Скачиваем файл
                    await api.download_attachment(attachment)
                    # Путь к файлу:
                    attachment_source = attachment.name

                    # Отправляем файл
                    attach = await DocMessagesUploader(api=message.ctx_api).upload(file_source = attachment_source,title = attachment.name ,peer_id=message.peer_id)
                    await message.answer(attachment=attach)

                    # Удаляем файл
                    os.remove(attachment_source)


                # Делаем пробел между объявлениями
                await message.answer('&#12288;')

        # Если нет объявлений:
        else:
            await message.answer('❌Нет объявлений!')

        await api.logout()
    except: # если произошла ошибка
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        await api.logout()
        return