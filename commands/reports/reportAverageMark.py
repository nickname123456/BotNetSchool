from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('reportAverageMark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportAverageMark'})
async def private_reportAverageMark(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMark')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)
    
    reportAverageMark = await ns.getReportAverageMark( # Получаем отчет
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )
    for i in reportAverageMark:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMark')


@bp.on.chat_message(payload={'cmd': 'reportAverageMark'})
async def chat_reportAverageMark(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMark')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    reportAverageMark = await ns.getReportAverageMark( # Получаем отчет
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )
    for i in reportAverageMark:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMark')