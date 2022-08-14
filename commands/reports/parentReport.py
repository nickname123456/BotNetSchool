from typing import Text
from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
import ns
from PostgreSQLighter import db
from VKRules import PayloadStarts


bp = Blueprint('parentReport') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(payload={'cmd': 'parentReport'})
async def private_parentReport(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    user_id = message.from_id # ID юзера
    
    terms = await ns.getTerms( # Получаем триместры/четверти
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )

    keyboard = Keyboard()
    for i in terms.keys(): # Перебираем триместры/четверти
        keyboard.add(Text(i, {'cmd': f'parentReport_{terms[i]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери триместр/четверть', keyboard=keyboard)

@bp.on.chat_message(payload={'cmd': 'parentReport'})
async def chat_parentReport(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport')
    # Айди чата:
    chat_id = message.chat_id
    
    terms = await ns.getTerms( # Получаем триместры/четверти
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    keyboard = Keyboard()
    for i in terms.keys(): # перебираем триместры/четверти
        keyboard.add(Text(i, {'cmd': f'parentReport_{terms[i]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text('Назад', {'cmd': 'reports'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери триместр/четверть', keyboard=keyboard)
    
    
    


@bp.on.private_message(PayloadStarts='{"cmd":"parentReport_')
async def private_parentReport_with_term(message: Message):
    logging.info(f'{message.peer_id}: I get parentReport with term')
    user_id = message.from_id # ID юзера

    termId = message.payload[21:-2] # ID триместра/четверти
    
    parentReport = await ns.getParentReport( # Получаем отчёт
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id),
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
    
    termId = message.payload[21:-2] # ID триместра/четверти
    
    parentReport = await ns.getParentReport( # Получаем отчет
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id),
        termId
    )
    for i in parentReport:
        await message.answer(i)
    logging.info(f'{message.peer_id}: I sent parentReport')