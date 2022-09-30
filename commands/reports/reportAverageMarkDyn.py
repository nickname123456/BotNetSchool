from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('reportAverageMarkDyn') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reportAverageMarkDyn'})
async def private_reportAverageMarkDyn(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMarkDyn')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)
    
    reportAverageMarkDyn = await ns.getReportAverageMarkDyn( # Получаем отчет
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )
    for i in reportAverageMarkDyn:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMarkDyn')


@bp.on.chat_message(payload={'cmd': 'reportAverageMarkDyn'})
async def chat_reportAverageMarkDyn(message: Message):
    logging.info(f'{message.peer_id}: I get reportAverageMarkDyn')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    reportAverageMarkDyn = await ns.getReportAverageMarkDyn( # Получаем отчет
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )
    for i in reportAverageMarkDyn:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent reportAverageMarkDyn')