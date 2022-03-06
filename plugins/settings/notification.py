from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import getMarkNotify, getAnnouncementsNotify
import asyncio
import logging


bp = Blueprint('notification')# Объявляем команду
db = SQLighter('database.db') # Подключаемся к базеданных
bp.on.vbml_ignore_case = True # Игнорируем регистр


@bp.on.message(text=["Уведы", "Уведомления"])
@bp.on.message(payload={'cmd': 'notification'})
async def notification_private(message: Message):
    logging.info(f'{message.peer_id}: I get notification')
    users = db.get_accounts_mark_notification()

    logging.info(f'{message.peer_id}: Started mailing')


    while True:

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
                for mark in result:
                    await bp.api.messages.send(message=mark, user_id=user_id, random_id=0)
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
                for announcement in result:
                    await bp.api.messages.send(message=announcement, user_id=user_id, random_id=0)			
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
            for mark in result:
                await bp.api.messages.send(message=mark, peer_id=2000000000+chat_id, random_id=0)
                await asyncio.sleep(1)
            #except Exception as e:
            #    pass
        
        
        chats = db.get_chats_mark_notification()
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
            for announcement in result:
                await bp.api.messages.send(message=announcement, peer_id=2000000000+chat_id, random_id=0)			
                await asyncio.sleep(1)
            #except Exception as e:
            #    pass



            logging.info(f'{message.peer_id}:I sleep for 30 minutes')
            asyncio.sleep(1800)