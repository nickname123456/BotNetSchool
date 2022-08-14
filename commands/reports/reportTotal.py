from vkbottle.bot import Message, Blueprint
import logging
import ns
from PostgreSQLighter import db


bp = Blueprint('reportTotal') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportTotal'})
async def private_reportTotal(message: Message):
    logging.info(f'{message.peer_id}: I get reportTotal')
    user_id = message.from_id # ID юзера

    reportTotal = await ns.getReportTotal( # Получаем отчет
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )
    for i in reportTotal:
        await message.answer(reportTotal[i])
    logging.info(f'{message.peer_id}: I sent reportTotal')


@bp.on.chat_message(payload={'cmd': 'reportTotal'})
async def chat_reportTotal(message: Message):
    logging.info(f'{message.peer_id}: I get reportTotal')
    # Айди чата:
    chat_id = message.chat_id
    
    reportTotal = await ns.getReportTotal( # Получаем отчет
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    for i in reportTotal:
        await message.answer(reportTotal[i])
    logging.info(f'{message.peer_id}: I sent reportTotal')