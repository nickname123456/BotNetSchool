from PostgreSQLighter import SQLighter
from ns import getMarkNotify, getAnnouncementsNotify
import asyncio
import logging
from settings import admin_id



db = SQLighter('database.db') # Подключаемся к базеданных




async def notification(bot):
    logging.info(f'Started mailing')

    try:
        users = db.get_accounts_mark_notification()
        for user in users:
            #try:
            if user[7]:
                user_id = user[0]
                marks, result = await getMarkNotify(
                    db.get_account_login(user_id),
                    db.get_account_password(user_id),
                    db.get_account_school(user_id),
                    db.get_account_link(user_id),
                    db.get_account_old_mark(user_id)
                )

                db.edit_account_old_mark(user_id, marks)
                db.commit()
                for mark in result:
                    await bot.api.messages.send(message=mark, user_id=user_id, random_id=0)
                    await asyncio.sleep(1)	
            #except Exception as e:
            #    pass
        

        users = db.get_accounts_announcements_notification()
        for user in users:
            #try:
            if user[7]:
                user_id = user[0]
                announcements, result = await getAnnouncementsNotify(
                    db.get_account_login(user_id),
                    db.get_account_password(user_id),
                    db.get_account_school(user_id),
                    db.get_account_link(user_id),
                    db.get_account_old_announcements(user_id)
                )

                db.edit_account_old_announcements(user_id, announcements)
                db.commit()
                for announcement in result:
                    await bot.api.messages.send(message=announcement, user_id=user_id, random_id=0)			
                    await asyncio.sleep(1)
            #except Exception as e:
            #    pass





        chats = db.get_chats_mark_notification()
        for chat in chats:
            #try:
            chat_id = chat[0]
            marks, result = await getMarkNotify(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_old_mark(chat_id)
            )

            db.edit_chat_old_mark(chat_id, marks)
            db.commit()
            for mark in result:
                await bot.api.messages.send(message=mark, peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)
            #except Exception as e:
            #    pass
        
        
        chats = db.get_chats_announcements_notification()
        for chat in chats:
            #try:
            chat_id = chat[0]
            announcements, result = await getAnnouncementsNotify(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_old_announcements(chat_id)
            )

            db.edit_chat_old_announcements(chat_id, announcements)
            db.commit()
            for announcement in result:
                await bot.api.messages.send(message=announcement, peer_id=2000000000+chat_id, random_id=0)			
                await asyncio.sleep(1)
            #except Exception as e:
            #    pass



        logging.info(f'I sleep for 10 minutes')
        #await asyncio.sleep(600)

    except:
        await bot.api.messages.send(message='У нас тут это... Ошибка в РАССЫЛКЕ!!! \nЧЕКАЙ ХЕРОКУ ЛОГИ', user_id=admin_id, random_id=0)