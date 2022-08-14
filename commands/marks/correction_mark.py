from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import ns
import logging


bp = Blueprint('correction_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark'})
async def private_correction_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark')
    user_id = message.from_id # ID юзера

    if message.text == '5️⃣':
        mark = 5
    elif message.text == '4️⃣':
        mark = 4
    elif message.text == '3️⃣':
        mark = 3

    db.edit_account_correction_mark(user_id, mark) # Изменяем желаемую оценку в бд
    db.commit()

    await message.answer(await ns.correction_mark(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id),
        db.get_account_correction_lesson(user_id),
        db.get_account_correction_mark(user_id)
    ))
    logging.info(f'{message.peer_id}: I sent correction_mark')











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

    db.edit_chat_correction_mark(chat_id, mark) # Изменяем желаемую оценку в бд
    db.commit()

    await message.answer(await ns.correction_mark(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id),
        db.get_chat_correction_lesson(chat_id),
        db.get_chat_correction_mark(chat_id)
    ))
    logging.info(f'{message.peer_id}: I sent correction_mark')