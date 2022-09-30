from database.methods.update import edit_chat_correction_mark, edit_student_correction_mark
from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('correction_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'correction_mark'})
async def private_correction_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark')
    user_id = message.from_id # ID юзера
    student = get_student_by_vk_id(user_id)

    if message.text == '5️⃣':
        mark = 5
    elif message.text == '4️⃣':
        mark = 4
    elif message.text == '3️⃣':
        mark = 3

    edit_student_correction_mark(vk_id=user_id, new_correction_mark=mark) # Изменяем желаемую оценку в бд

    numLesson = int(student.correction_lesson)
    lesson = (await ns.get_marks( # Получаем уроки
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        onlySubjects= True
    ))[numLesson]

    await message.answer(await ns.correction_mark(
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        lesson,
        int(student.correction_mark)
    ))
    logging.info(f'{message.peer_id}: I sent correction_mark')











@bp.on.chat_message(payload={'cmd': 'correction_mark'})
async def chat_correction_mark(message: Message):
    logging.info(f'{message.peer_id}: I get correction_mark')
    # Айди чата:
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    if message.text == '5️⃣':
        mark = 5
    elif message.text == '4️⃣':
        mark = 4
    elif message.text == '3️⃣':
        mark = 3

    edit_chat_correction_mark(vk_id=chat_id, new_correction_mark=mark) # Изменяем желаемую оценку в бд

    numLesson = int(chat.correction_lesson)
    lesson = (await ns.get_marks( # Получаем уроки
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId,
        onlySubjects= True
    ))[numLesson]

    await message.answer(await ns.correction_mark(
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId,
        lesson,
        int(chat.correction_mark)
    ))
    logging.info(f'{message.peer_id}: I sent correction_mark')