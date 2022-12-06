from database.methods.get import get_chat_by_vk_id, get_homework, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging


bp = Blueprint('homework') # Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts




@bp.on.private_message(PayloadStarts='{"cmd":"homework_')
async def private_homework(message: Message):
    logging.info(f'{message.peer_id}: I get homework')
    userId = message.from_id # ID юзера
    student = get_student_by_vk_id(userId)

    if (await bp.state_dispenser.get(message.from_id)): 
        if message.from_id == (await bp.state_dispenser.get(message.from_id)).peer_id:
            await bp.state_dispenser.delete(message.from_id) # Удаляем цепочку состояний

    lessons = await ns.getSubjectsId(
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )

    lessonId = message.payload[17:-2]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]
    
    # Получаем дз
    homework = get_homework(lesson, student.school, student.clas)

    if homework:
        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
        logging.info(f'{message.peer_id}: Send homework')
    else:
        await message.answer('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')



@bp.on.chat_message(PayloadStarts='{"cmd":"homework_')
async def chat_homework(message: Message):
    logging.info(f'{message.peer_id}: I get homework')
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    lessons = await ns.getSubjectsId(
        chat.login,
        chat.password,
        chat.school,
        chat.link,
        chat.studentId
    )

    lessonId = message.payload[17:-2]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]

    # Получаем дз
    homework = get_homework(lesson, chat.school, chat.clas)

    if homework:
        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
        logging.info(f'{message.peer_id}: Send homework')
    else:
        await message.answer('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')