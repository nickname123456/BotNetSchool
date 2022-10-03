from database.methods.update import edit_chat_studentId, edit_student_studentId
from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
from vk_bot.commands.change_anything import change_anything_kb
import ns

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging


bp = Blueprint('change_student')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts





@bp.on.private_message(payload={'cmd': 'change_student'})
async def private_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    students = await ns.getStudents( # Получаем всех детей, привязанных к аккаунту СГО
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )
    currentStudentId = student.studentId # Получаем выбранного ребенка
    
    keyboard = Keyboard()
    for i in students: # Перебираем детей
        if i['studentId'] == currentStudentId: # Если этот ребенок - выбранный, то выделяем зеленым
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        else:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
            keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите ребенка', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent change_student')

@bp.on.chat_message(payload={'cmd': 'change_student'})
async def chat_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    students = await ns.getStudents( # Получаем всех детей, привязанных к аккаунту СГО
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )
    currentStudentId = chat.studentId # Получаем выбранного ребенка
    
    keyboard = Keyboard()
    for i in students: # Перебираем детей
        if i['studentId'] == currentStudentId:  # Если ребенок - выбраный, то выделяем зеленым цветом
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        else:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
            keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('👆🏻Выберите ребенка', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent change_student')


@bp.on.private_message(PayloadStarts='{"cmd":"change_student_')
async def private_exactly_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    user_id = message.from_id # ID юзера

    studentId = message.payload[23:-2] # Получаем ID ученика, на котого сменили

    edit_student_studentId(vk_id=user_id, new_studentId=studentId) # Меняем в бд выбранного ребенка

    await message.answer('✅Я успешно сменил выбранного ребенка')
    logging.info(f'{message.peer_id}: I sent change_student with studentId')
    await change_anything_kb.change_anything_kb(message)

@bp.on.chat_message(PayloadStarts='{"cmd":"change_student_')
async def chat_exactly_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    # Айди чата:
    chat_id = message.chat_id

    studentId = message.payload[23:-2] # Получаем ID ученика, на которого сменили

    edit_chat_studentId(vk_id=chat_id, new_studentId=studentId) # Меняем в бд выбранного ребенка

    await message.answer('✅Я успешно сменил выбранного ребенка')
    logging.info(f'{message.peer_id}: I sent change_student with studentId')
    await change_anything_kb.change_anything_kb(message)