from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('reportTotal') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportTotal'})
async def private_reportTotal(message: Message):
    logging.info(f'{message.peer_id}: I get reportTotal')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    reportTotal = await ns.getReportTotal( # Получаем отчет
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )
    for i in reportTotal:
        await message.answer(reportTotal[i])
    logging.info(f'{message.peer_id}: I sent reportTotal')


@bp.on.chat_message(payload={'cmd': 'reportTotal'})
async def chat_reportTotal(message: Message):
    logging.info(f'{message.peer_id}: I get reportTotal')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    reportTotal = await ns.getReportTotal( # Получаем отчет
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )
    for i in reportTotal:
        await message.answer(reportTotal[i])
    logging.info(f'{message.peer_id}: I sent reportTotal')