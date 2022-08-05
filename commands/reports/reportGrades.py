from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
import ns
from PostgreSQLighter import db
from VKRules import PayloadStarts


bp = Blueprint('reportGrades') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(payload={'cmd': 'reportGrades'})
async def private_reportGrades(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id
    
    subjects = await ns.getSubjectsId(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )

    keyboard = Keyboard()
    counter = 0
    for i in subjects.keys():
        if counter == 4:
            keyboard.row()
            counter = 0
        keyboard.add(Text(i, {'cmd': f'reportGrades_{subjects[i]}'}), color=KeyboardButtonColor.SECONDARY)
        counter += 1
        
    keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери урок', keyboard=keyboard)

@bp.on.chat_message(payload={'cmd': 'reportGrades'})
async def chat_reportGrades(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades')
    # Айди чата:
    chat_id = message.chat_id
    
    subjects = await ns.getSubjectsId(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    keyboard = Keyboard()
    counter = 0
    for i in subjects.keys():
        if counter == 4:
            keyboard.row()
            counter = 0
        keyboard.add(Text(i, {'cmd': f'reportGrades_{subjects[i]}'}), color=KeyboardButtonColor.SECONDARY)
        counter += 1
        
    keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери урок', keyboard=keyboard)



@bp.on.private_message(PayloadStarts='{"cmd":"reportGrades_')
async def private_reportGrades_with_sub(message: Message):
    logging.info(f'{message.peer_id}: I get reportGrades with term')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    subjectId = message.payload[21:-2]
    
    reportGrades = await ns.getReportGrades(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id),
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

    subjectId = message.payload[21:-2]
    
    reportGrades = await ns.getReportGrades(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id),
        subjectId
    )
    for i in reportGrades:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')