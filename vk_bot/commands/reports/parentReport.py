from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging


bp = Blueprint('parentReport') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(payload={'cmd': 'parentReport'})
async def private_parentReport(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)
    
    terms = await ns.getTerms( # Получаем триместры/четверти
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )

    keyboard = Keyboard()
    for i in terms.keys(): # Перебираем триместры/четверти
        keyboard.add(Text(i, {'cmd': f'parentReport_{terms[i]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите триместр/четверть', keyboard=keyboard)

@bp.on.chat_message(payload={'cmd': 'parentReport'})
async def chat_parentReport(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    terms = await ns.getTerms( # Получаем триместры/четверти
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )

    keyboard = Keyboard()
    for i in terms.keys(): # перебираем триместры/четверти
        keyboard.add(Text(i, {'cmd': f'parentReport_{terms[i]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите триместр/четверть', keyboard=keyboard)
    
    
    


@bp.on.private_message(PayloadStarts='{"cmd":"parentReport_')
async def private_parentReport_with_term(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport with term')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    termId = message.payload[21:-2] # ID триместра/четверти
    
    parentReport = await ns.getParentReport( # Получаем отчёт
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        termId
    )
    for i in parentReport:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')


@bp.on.chat_message(PayloadStarts='{"cmd":"parentReport_')
async def chat_parentReport_with_term(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport with term')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    termId = message.payload[21:-2] # ID триместра/четверти
    
    parentReport = await ns.getParentReport( # Получаем отчет
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId,
        termId
    )
    for i in parentReport:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')