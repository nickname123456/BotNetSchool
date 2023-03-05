from database.methods.delete import delete_chat
from database.methods.get import get_chats_with_announcements_notification, get_chats_with_mark_notification, get_students_with_announcements_notification, get_students_with_mark_notification
from database.methods.update import edit_student_old_announcements, edit_student_old_mark, edit_chat_old_announcements, edit_chat_old_mark, edit_student_telegram_id, edit_student_vk_id

from ns import getMarkNotify, getAnnouncementsNotify

from tg_bot.utils import send_telegram_msg, send_telegram_bytes_file

from settings import admin_id
from settings import tg_token

from vkbottle import DocMessagesUploader, VKAPIError
import aiogram

import asyncio
import logging

tg_bot = aiogram.Bot(token=tg_token, parse_mode='HTML')

async def notification(bot):
    logging.info(f'Started mailing')

    try:
        users = get_students_with_mark_notification() # Получаем юзеров, подписанных на новые оценки
        for user in users:
            telegram_id = user.telegram_id
            vk_id = user.vk_id
            try:
                marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                    user.login,
                    user.password,
                    user.school,
                    user.link,
                    user.old_mark
                )
                logging.info(f'I got {len(result)} new marks for user vk_id={vk_id}, telegram_id={telegram_id}')
            except:
                logging.error(f'Error while getting marks for user vk_id={vk_id}, telegram_id={telegram_id}')
                continue

            if vk_id:
                edit_student_old_mark(vk_id=vk_id, new_old_mark=str(marks)) # Говорим бд все текущие оценки
            elif telegram_id:
                edit_student_old_mark(telegram_id=telegram_id, new_old_mark=str(marks)) # Говорим бд все текущие оценки

            for mark in result[-5:]: # Берем только последние 5 оценок из новых, чтобы не спамить
                if vk_id:
                    try: # Пытаемся отправить оценку в вк
                        await bot.api.messages.send(message=mark, user_id=vk_id, random_id=0)
                        logging.info(f'I send mark notify to vk user. Id: {vk_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send mark notify to vk user. Id: {vk_id}')
                        continue
                    await asyncio.sleep(1)
                if telegram_id:
                    try: # Пытаемся отправить оценку в телеграм
                        await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=mark)
                        logging.info(f'I send mark notify to telegram user. Id: {telegram_id}')
                    except:
                        logging.error(f'I cannot send mark notify to telegram user. Id: {telegram_id}')
                        continue
                    await asyncio.sleep(1)
        

        users = get_students_with_announcements_notification() # Получаем юзеров, которые подписаны на новые объявления
        for user in users:
            telegram_id = user.telegram_id
            vk_id = user.vk_id
            try:
                announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                    user.login,
                    user.password,
                    user.school,
                    user.link,
                    user.studentId,
                    user.old_announcements
                )
                logging.info(f'I got {len(result)} new announcements for chat vk_id={vk_id}, telegram_id={telegram_id}')
            except:
                logging.error(f'Error while getting new announcements for chat vk_id={vk_id}, telegram_id={telegram_id}')
                continue

            if vk_id:
                edit_student_old_announcements(vk_id=vk_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            elif telegram_id:
                edit_student_old_announcements(telegram_id=telegram_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            
            for announcement in result[:3]: # Отправляем 3 последних объявления
                if vk_id:
                    try: # Пытаемся отправить объявление в вк
                        await bot.api.messages.send(message=announcement['text'], user_id=vk_id, random_id=0)
                        for attachment in announcement['attachments']: # отправить вложения
                            attach = await DocMessagesUploader(api=bot.api).upload(
                                file_source = announcement['attachments'][attachment]['file_source'],
                                title = announcement['attachments'][attachment]['title'],
                                peer_id=vk_id)
                            await bot.api.messages.send(message=announcement['attachments'][attachment]['title'], attachment=attach,user_id=vk_id, random_id=0)
                        await bot.api.messages.send(message='&#12288;', user_id=vk_id, random_id=0)
                        logging.info(f'I send announcement notify to vk user. Id: {vk_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send announcement notify to vk user. Id: {vk_id}')
                        continue
                    await asyncio.sleep(1)
                if telegram_id:
                    try: # Пытаемся отправить объявление в телеграм
                        reply_to_message_id = (await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=announcement['text']))['message_id']
                        for attachment in announcement['attachments']: # отправить вложения
                            await send_telegram_bytes_file(bot=tg_bot, chat_id=telegram_id, file=announcement['attachments'][attachment]['file_source'], caption=announcement['attachments'][attachment]['title'], reply_to_message_id=reply_to_message_id)
                        logging.info(f'I send announcement notify to telegram user. Id: {telegram_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send announcement notify to telegram user. Id: {telegram_id}')
                        continue
                    await asyncio.sleep(1)





        chats = get_chats_with_mark_notification() # Получаем все чаты, подписанные на новые оценки
        for chat in chats:
            vk_id = chat.vk_id
            telegram_id = chat.telegram_id
            try:
                marks, result = await getMarkNotify( # Получаем все оценки и те из них, которые новые
                    chat.login,
                    chat.password,
                    chat.school,
                    chat.link,
                    chat.old_mark
                )
                logging.info(f'I got {len(result)} new marks for chat vk_id={vk_id}, telegram_id={telegram_id}')
            except:
                logging.error(f'Error while getting marks for chat vk_id={vk_id}, telegram_id={telegram_id}')
                continue

            if vk_id:
                edit_chat_old_mark(vk_id=vk_id, new_old_mark=str(marks)) # Обновляем старые оценки
            elif telegram_id:
                edit_chat_old_mark(telegram_id=telegram_id, new_old_mark=str(marks)) # Обновляем старые оценки
            
            for mark in result[-5:]: # Отправляем только 5 последних новых оценок, чтобы сильно не спамить
                if vk_id:
                    try: # Пытаемся отправить оценку в вк
                        await bot.api.messages.send(message=mark, peer_id=2000000000+vk_id, random_id=0)
                        logging.info(f'I send mark notify to vk chat. Id: {vk_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send mark notify to vk chat. Id: {vk_id}')
                        continue
                    await asyncio.sleep(1)
                if telegram_id:
                    try: # Пытаемся отправить оценку в телеграм
                        await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=mark)
                        logging.info(f'I send mark notify to telegram chat. Id: {telegram_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send mark notify to telegram chat. Id: {telegram_id}')
                        continue
                    await asyncio.sleep(1)       
        



        chats = get_chats_with_announcements_notification() # Получаем чаты, подписанные на новые объявления
        for chat in chats:
            vk_id = chat.vk_id
            telegram_id = chat.telegram_id
            try:
                announcements, result = await getAnnouncementsNotify( # Получаем все объявления и те из них, которые новые
                    chat.login,
                    chat.password,
                    chat.school,
                    chat.link,
                    chat.studentId,
                    chat.old_announcements
                )
                logging.info(f'I got {len(result)} new announcements for chat vk_id={vk_id}, telegram_id={telegram_id}')
            except:
                logging.error(f'Error while getting announcements for chat vk_id={vk_id}, telegram_id={telegram_id}')
                continue
            
            if vk_id:
                edit_chat_old_announcements(vk_id=vk_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            elif telegram_id:
                edit_chat_old_announcements(telegram_id=telegram_id, new_old_announcements=str(list(announcements.keys()))) # Сообщаем бд все объвления
            
            for announcement in result[:3]: # Отправляем 3 последних объявления, чтобы сильно не спамить
                if vk_id:
                    try: # Пытаемся отправить объявление в вк
                        await bot.api.messages.send(message=announcement['text'], peer_id=2000000000+vk_id, random_id=0)
                        for attachment in announcement['attachments']: # отправить вложения
                            attach = await DocMessagesUploader(api=bot.api).upload(
                                file_source = announcement['attachments'][attachment]['file_source'],
                                title = announcement['attachments'][attachment]['title'],
                                peer_id=2000000000+vk_id)
                            await bot.api.messages.send(message=announcement['attachments'][attachment]['title'], attachment=attach,peer_id=2000000000+vk_id, random_id=0)
                        await bot.api.messages.send(message='&#12288;', peer_id=2000000000+vk_id, random_id=0)
                        logging.info(f'I send announcement notify to vk chat. Id: {vk_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send announcement notify to vk chat. Id: {vk_id}')
                        continue
                    await asyncio.sleep(1)
                if telegram_id:
                    try: # Пытаемся отправить объявление в телеграм
                        reply_to_message_id = (await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=announcement['text']))['message_id']
                        for attachment in announcement['attachments']: # отправить вложения
                            await send_telegram_bytes_file(bot=tg_bot, chat_id=telegram_id, file=announcement['attachments'][attachment]['file_source'], caption=announcement['attachments'][attachment]['title'], reply_to_message_id=reply_to_message_id)
                        logging.info(f'I send announcement notify to telegram chat. Id: {telegram_id}')
                    except: # Если не получилось отправить
                        logging.error(f'I cannot send announcement notify to telegram chat. Id: {telegram_id}')
                        continue
                    await asyncio.sleep(1)

        logging.info(f'I sleep for 10 minutes')

    except Exception as e:
        logging.error(f'Error in notification: {e}')
        await bot.api.messages.send(message=f'У нас тут это... Ошибка в РАССЫЛКЕ!!! \n{e} \nЧЕКАЙ ЛОГИ', user_id=admin_id, random_id=0)
        raise