from vkbottle.bot import Message, Blueprint
import logging
import ns
from PostgreSQLighter import db


bp = Blueprint('reportAverageMark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportAverageMark'})
async def private_reportAverageMark(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMark')
    user_id = message.from_id # ID юзера
    
    reportAverageMark = await ns.getReportAverageMark( # Получаем отчет
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )
    for i in reportAverageMark:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMark')


@bp.on.chat_message(payload={'cmd': 'reportAverageMark'})
async def chat_reportAverageMark(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMark')
    # Айди чата:
    chat_id = message.chat_id
    
    reportAverageMark = await ns.getReportAverageMark( # Получаем отчет
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    for i in reportAverageMark:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMark')