from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
import ns
from PostgreSQLighter import db


bp = Blueprint('parentReport') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'parentReport'})
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    
    
    logging.info(f'{message.peer_id}: I sent parentReport')
    parentReport = await ns.getParentReport(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id)
    )
    for i in parentReport:
        await message.answer(i)


@bp.on.chat_message(payload={'cmd': 'parentReport'})
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    # Айди чата:
    chat_id = message.chat_id

    
    
    logging.info(f'{message.peer_id}: I sent parentReport')
    parentReport = await ns.getParentReport(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id)
    )
    for i in parentReport:
        await message.answer(i)