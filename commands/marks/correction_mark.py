from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import ns
import logging


bp = Blueprint('correction_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark'})
async def private_correction_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if message.text == '5️⃣':
        mark = 5
    elif message.text == '4️⃣':
        mark = 4
    elif message.text == '3️⃣':
        mark = 3

    db.edit_account_correction_mark(user_id, mark)
    db.commit()

    logging.info(f'{message.peer_id}: I sent correction_mark')
    await message.answer(await ns.correction_mark(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_correction_lesson(user_id),
        db.get_account_correction_mark(user_id),
        db.get_account_studentId(user_id)
    ))











@bp.on.chat_message(payload={'cmd': 'correction_mark'})
async def chat_correction_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark')
    # Айди чата:
    chat_id = message.chat_id

    if message.text == '5️⃣':
        mark = 5
    elif message.text == '4️⃣':
        mark = 4
    elif message.text == '3️⃣':
        mark = 3

    db.edit_chat_correction_mark(chat_id, mark)
    db.commit()

    logging.info(f'{message.peer_id}: I sent correction_mark')
    await message.answer(await ns.correction_mark(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_correction_lesson(chat_id),
        db.get_chat_correction_mark(chat_id),
        db.get_chat_studentId(chat_id)
    ))