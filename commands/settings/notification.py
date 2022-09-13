from PostgreSQLighter import db
from netschoolapi.errors import AuthError
from ns import getMarkNotify, getAnnouncementsNotify
import asyncio
import logging
from vkbottle import DocMessagesUploader
from settings import admin_id



async def notification(bot):
    logging.info(f'Started mailing')

    try:
        users = db.get_accounts_mark_notification() # Получаем юзеров, подписанных на новые оценки
        for user in users:
            if user[8]: # Проверка на правильный логин и пароль
                user_id = user[0]
                try:
                    marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                        db.get_account_login(user_id),
                        db.get_account_password(user_id),
                        db.get_account_school(user_id),
                        db.get_account_link(user_id),
                        db.get_account_old_mark(user_id)
                    )
                except AuthError:
                    await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=user_id, random_id=0)
                    continue

                db.edit_account_old_mark(user_id, marks) # Говорим бд все текущие оценки
                db.commit()
                for mark in result[-15:]: # Берем только последние 15 оценок из новых, чтобы не спамить
                    await bot.api.messages.send(message=mark, user_id=user_id, random_id=0)
                    await asyncio.sleep(1)
        

        users = db.get_accounts_announcements_notification() # Получаем юзеров, которые подписаны на новые объявления
        for user in users:
            if user[8]: # Проверка на правильный логин и пароль
                user_id = user[0]
                try:
                    announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                        db.get_account_login(user_id),
                        db.get_account_password(user_id),
                        db.get_account_school(user_id),
                        db.get_account_link(user_id),
                        db.get_account_studentId(user_id),
                        db.get_account_old_announcements(user_id)
                    )
                except AuthError:
                    await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=user_id, random_id=0)
                    continue

                db.edit_account_old_announcements(user_id, list(announcements.keys())) # Сообщаем бд все объвления
                db.commit()
                for announcement in result: # Отправляем все новые объявления
                    await bot.api.messages.send(message=announcement['text'], user_id=user_id, random_id=0)
                    for attachment in announcement['attachments']:
                        attach = await DocMessagesUploader(api=bot.api).upload(
                            file_source = announcement['attachments'][attachment]['file_source'],
                            title = announcement['attachments'][attachment]['title'],
                            peer_id=user_id)
                        await bot.api.messages.send(attachment=attach,user_id=user_id, random_id=0)
                    await bot.api.messages.send(message='&#12288;', user_id=user_id, random_id=0)
                    await asyncio.sleep(1)





        chats = db.get_chats_mark_notification() # Получаем все чаты, подписанные на новые оценки
        for chat in chats:
            chat_id = chat[0]
            try:
                marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новыеы
                    db.get_chat_login(chat_id),
                    db.get_chat_password(chat_id),
                    db.get_chat_school(chat_id),
                    db.get_chat_link(chat_id),
                    db.get_chat_old_mark(chat_id)
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=2000000000+chat_id, random_id=0)
                continue

            db.edit_chat_old_mark(chat_id, marks) # Говорим бд все оценки
            db.commit()
            for mark in result[-15:]: # Отправляем только 15 последних новых оценок, чтобы сильно не спамить
                await bot.api.messages.send(message=mark, peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)        
        
        chats = db.get_chats_announcements_notification() # Получаем чаты, подписанные на новые объявления
        for chat in chats:
            chat_id = chat[0]
            try:
                announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                    db.get_chat_login(chat_id),
                    db.get_chat_password(chat_id),
                    db.get_chat_school(chat_id),
                    db.get_chat_link(chat_id),
                    db.get_chat_studentId(chat_id),
                    db.get_chat_old_announcements(chat_id)
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых объявлений было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=2000000000+chat_id, random_id=0)
                continue

            db.edit_chat_old_announcements(chat_id, list(announcements.keys())) # Сообщаем бд все объвления
            db.commit()
            for announcement in result: # Отправляем все новые объявления
                await bot.api.messages.send(message=announcement['text'], peer_id=2000000000+chat_id, random_id=0)
                for attachment in announcement['attachments']:
                    attach = await DocMessagesUploader(api=bot.api).upload(
                        file_source = announcement['attachments'][attachment]['file_source'],
                        title = announcement['attachments'][attachment]['title'],
                        peer_id=2000000000+chat_id)
                    await bot.api.messages.send(attachment=attach,peer_id=2000000000+chat_id, random_id=0)
                await bot.api.messages.send(message='&#12288;', peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)

            logging.info(f'I sleep for 60 minutes')

    except Exception as e:
        await bot.api.messages.send(message=f'У нас тут это... Ошибка в РАССЫЛКЕ!!! \n{e} \nЧЕКАЙ ХЕРОКУ ЛОГИ', user_id=admin_id, random_id=0)