from vkbottle.bot import Message, Blueprint
import logging
import ns
from PostgreSQLighter import db


bp = Blueprint('reportAverageMarkDyn') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportAverageMarkDyn'})
async def private_reportAverageMarkDyn(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMarkDyn')
    user_id = message.from_id # ID юзера
    
    reportAverageMarkDyn = await ns.getReportAverageMarkDyn( # Получаем отчет
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )
    for i in reportAverageMarkDyn:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMarkDyn')


@bp.on.chat_message(payload={'cmd': 'reportAverageMarkDyn'})
async def chat_reportAverageMarkDyn(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMarkDyn')
    # Айди чата:
    chat_id = message.chat_id
    
    reportAverageMarkDyn = await ns.getReportAverageMarkDyn( # Получаем отчет
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    for i in reportAverageMarkDyn:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMarkDyn')