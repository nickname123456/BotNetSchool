from PostgreSQLighter import db
from ns import getMarkNotify, getAnnouncementsNotify
import asyncio
import logging



async def notification(bot):
    logging.info(f'Started mailing')

    #try:
    users = db.get_accounts_mark_notification() # Получаем юзеров, подписанных на новые оценки
    for user in users:
        #try:
        if user[8]: # Проверка на правильный логин и пароль
            user_id = user[0]
            marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                db.get_account_login(user_id),
                db.get_account_password(user_id),
                db.get_account_school(user_id),
                db.get_account_link(user_id),
                db.get_account_old_mark(user_id)
            )

            db.edit_account_old_mark(user_id, marks) # Говорим бд все текущие оценки
            db.commit()
            for mark in result[-15:]: # Берем только последние 15 оценок из новых, чтобы не спамить
                await bot.api.messages.send(message=mark, user_id=user_id, random_id=0)
                await asyncio.sleep(1)
    

    users = db.get_accounts_announcements_notification() # Получаем юзеров, которые подписаны на новые объявления
    for user in users:
        #try:
        if user[8]: # Проверка на правильный логин и пароль
            user_id = user[0]
            announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                db.get_account_login(user_id),
                db.get_account_password(user_id),
                db.get_account_school(user_id),
                db.get_account_link(user_id),
                db.get_account_studentId(user_id),
                db.get_account_old_announcements(user_id)
            )

            db.edit_account_old_announcements(user_id, announcements) # Сообщаем бд все объвления
            db.commit()
            for announcement in result: # Отправляем все новые объявления
                await bot.api.messages.send(message=announcement, user_id=user_id, random_id=0)			
                await asyncio.sleep(1)





    chats = db.get_chats_mark_notification() # Получаем все чаты, подписанные на новые оценки
    for chat in chats:
        #try:
        chat_id = chat[0]
        marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новыеы
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_old_mark(chat_id)
        )

        db.edit_chat_old_mark(chat_id, marks) # Говорим бд все оценки
        db.commit()
        for mark in result[-15:]: # Отправляем только 15 последних новых оценок, чтобы сильно не спамить
            await bot.api.messages.send(message=mark, peer_id=2000000000+chat_id, random_id=0)
            await asyncio.sleep(1)        
    
    chats = db.get_chats_announcements_notification() # Получаем чаты, подписанные на новые объявления
    for chat in chats:
        chat_id = chat[0]
        announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_studentId(chat_id),
            db.get_chat_old_announcements(chat_id)
        )

        db.edit_chat_old_announcements(chat_id, announcements) # Говорим бд все объявления
        db.commit()
        for announcement in result: # Отправляем все новые объявления
            await bot.api.messages.send(message=announcement, peer_id=2000000000+chat_id, random_id=0)			
            await asyncio.sleep(1)

        logging.info(f'I sleep for 60 minutes')

    #except:
    #    await bot.api.messages.send(message='У нас тут это... Ошибка в РАССЫЛКЕ!!! \nЧЕКАЙ ХЕРОКУ ЛОГИ', user_id=admin_id, random_id=0)