from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging


bp = Blueprint('reportGrades') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(payload={'cmd': 'reportGrades'})
async def private_reportGrades(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)
    
    subjects = await ns.getSubjectsId( # Получаем ID урока
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )

    keyboard = Keyboard()
    counter = 0
    for i in subjects.keys(): # Перебираем уроки
        if counter == 4: # Если в строке уже 4 урока, то переходим на след строку
            keyboard.row()
            counter = 0
        keyboard.add(Text(i[:40], {'cmd': f'reportGrades_{subjects[i]}'}), color=KeyboardButtonColor.SECONDARY)
        counter += 1
        
    keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите урок', keyboard=keyboard)

@bp.on.chat_message(payload={'cmd': 'reportGrades'})
async def chat_reportGrades(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)
    
    subjects = await ns.getSubjectsId( # Получаем ID урока
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )

    keyboard = Keyboard()
    counter = 0
    for i in subjects.keys(): # Перебираем уроки
        if counter == 4: # Если на строке уже 4 урока, переходим на след строку
            keyboard.row()
            counter = 0
        keyboard.add(Text(i[:40], {'cmd': f'reportGrades_{subjects[i]}'}), color=KeyboardButtonColor.SECONDARY)
        counter += 1
        
    keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите урок', keyboard=keyboard)



@bp.on.private_message(PayloadStarts='{"cmd":"reportGrades_')
async def private_reportGrades_with_sub(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades with term')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    subjectId = message.payload[21:-2] # Получаем ID урока
    
    reportGrades = await ns.getReportGrades( # Получаем отчеты
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        subjectId
    )
    for i in reportGrades:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')

@bp.on.chat_message(PayloadStarts='{"cmd":"reportGrades_')
async def chat_reportGrades_with_sub(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades with term')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    subjectId = message.payload[21:-2] # Получаем ID урока
    
    reportGrades = await ns.getReportGrades( # Получаем отчет
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId,
        subjectId
    )
    for i in reportGrades:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')