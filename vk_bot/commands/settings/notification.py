from database.methods.get import get_chats_with_announcements_notification, get_chats_with_mark_notification, get_students_with_announcements_notification, get_students_with_mark_notification
from database.methods.update import edit_student_old_announcements, edit_student_old_mark, edit_chat_old_announcements, edit_chat_old_mark
from ns import getMarkNotify, getAnnouncementsNotify
from netschoolapi.errors import AuthError
from settings import admin_id

from vkbottle import DocMessagesUploader

import asyncio
import logging



async def notification(bot):
    logging.info(f'Started mailing')

    try:
        users = get_students_with_mark_notification() # Получаем юзеров, подписанных на новые оценки
        for user in users:
            user_id = user.vk_id
            try:
                marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                    user.login,
                    user.password,
                    user.school,
                    user.link,
                    user.old_mark
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=user_id, random_id=0)
                continue
            
            edit_student_old_mark(vk_id=user_id, new_old_mark=str(marks)) # Говорим бд все текущие оценки
            for mark in result[-15:]: # Берем только последние 15 оценок из новых, чтобы не спамить
                await bot.api.messages.send(message=mark, user_id=user_id, random_id=0)
                await asyncio.sleep(1)
        

        users = get_students_with_announcements_notification() # Получаем юзеров, которые подписаны на новые объявления
        for user in users:
            user_id = user.vk_id
            try:
                announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                    user.login,
                    user.password,
                    user.school,
                    user.link,
                    user.studentId,
                    user.old_announcements
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=user_id, random_id=0)
                continue

            edit_student_old_announcements(vk_id=user_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            for announcement in result: # Отправляем все новые объявления
                await bot.api.messages.send(message=announcement['text'], user_id=user_id, random_id=0)
                for attachment in announcement['attachments']:
                    attach = await DocMessagesUploader(api=bot.api).upload(
                        file_source = announcement['attachments'][attachment]['file_source'],
                        title = announcement['attachments'][attachment]['title'],
                        peer_id=user_id)
                    await bot.api.messages.send(message=announcement['attachments'][attachment]['title'], attachment=attach,user_id=user_id, random_id=0)
                await bot.api.messages.send(message='&#12288;', user_id=user_id, random_id=0)
                await asyncio.sleep(1)





        chats = get_chats_with_mark_notification() # Получаем все чаты, подписанные на новые оценки
        for chat in chats:
            chat_id = chat.vk_id
            try:
                marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                    chat.login,
                    chat.password,
                    chat.school,
                    chat.link,
                    chat.old_mark
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых оценок было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=2000000000+chat_id, random_id=0)
                continue

            edit_chat_old_mark(vk_id=chat_id, new_old_mark=str(marks))
            for mark in result[-15:]: # Отправляем только 15 последних новых оценок, чтобы сильно не спамить
                await bot.api.messages.send(message=mark, peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)        
        
        chats = get_chats_with_announcements_notification() # Получаем чаты, подписанные на новые объявления
        for chat in chats:
            chat_id = chat.vk_id
            try:
                announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                    chat.login,
                    chat.password,
                    chat.school,
                    chat.link,
                    chat.studentId,
                    chat.old_announcements
                )
            except AuthError:
                await bot.api.messages.send(message='❌При рассылке новых объявлений было выявлено, что у вас неправильный логин или пароль! \n🤔Настоятельно рекомендую написать "Начать", чтобы пройти регистрацию еще раз', peer_id=2000000000+chat_id, random_id=0)
                continue

            edit_chat_old_announcements(vk_id=chat_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            for announcement in result: # Отправляем все новые объявления
                await bot.api.messages.send(message=announcement['text'], peer_id=2000000000+chat_id, random_id=0)
                for attachment in announcement['attachments']:
                    attach = await DocMessagesUploader(api=bot.api).upload(
                        file_source = announcement['attachments'][attachment]['file_source'],
                        title = announcement['attachments'][attachment]['title'],
                        peer_id=2000000000+chat_id)
                    await bot.api.messages.send(message=announcement['attachments'][attachment]['title'], attachment=attach,peer_id=2000000000+chat_id, random_id=0)
                await bot.api.messages.send(message='&#12288;', peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)

            logging.info(f'I sleep for 10 minutes')

    except Exception as e:
        await bot.api.messages.send(message=f'У нас тут это... Ошибка в РАССЫЛКЕ!!! \n{e} \nЧЕКАЙ ХЕРОКУ ЛОГИ', user_id=admin_id, random_id=0)