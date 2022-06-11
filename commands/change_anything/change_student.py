from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
import ns
from VKRules import PayloadStarts
from commands.change_anything.change_anything_kb import change_anything_kb


bp = Blueprint('change_student')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts





@bp.on.private_message(payload={'cmd': 'change_student'})
async def menu(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    students = await ns.getStudents(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )
    
    keyboard = Keyboard()
    for i in students:
        keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери ребенка', keyboard=keyboard)

@bp.on.chat_message(payload={'cmd': 'change_student'})
async def menu(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    # Айди чата:
    chat_id = message.chat_id

    students = await ns.getStudents(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    
    keyboard = Keyboard()
    for i in students:
        keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери ребенка', keyboard=keyboard)


@bp.on.private_message(PayloadStarts='{"cmd":"change_student_')
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    studentId = message.payload[23:-2]

    db.edit_account_studentId(user_id, studentId)

    await message.answer('Я успешно сменил выбрнного ребенка')
    await change_anything_kb(message)

@bp.on.chat_message(PayloadStarts='{"cmd":"change_student_')
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    # Айди чата:
    chat_id = message.chat_id

    studentId = message.payload[23:-2]

    db.edit_chat_studentId(chat_id, studentId)

    await message.answer('Я успешно сменил выбрнного ребенка')
    await change_anything_kb(message)