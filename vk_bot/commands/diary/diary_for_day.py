from database.methods.get import get_chat_by_vk_id, get_homework, get_student_by_vk_id
from ns import get_back_week, get_next_week, get_week, get_diary
import netschoolapi

from vkbottle.bot import Blueprint, Message
from misc.VKRules import PayloadStarts

import logging


bp = Blueprint('diary_for_day') # Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts


@bp.on.private_message(PayloadStarts=['{"cmd":"next_diary_for_day', 
    '{"cmd":"back_diary_for_day', 
    '{"cmd":"diary_for_day'])
async def private_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    userId = message.from_id # ID юзера
    student = get_student_by_vk_id(userId)

    # Если пользователь выбрал текущую неделю
    if message.payload.startswith('{"cmd":"diary_for_day_'):
        week = get_week()
        day = int(message.payload[22:-2])
    # Если пользователь выбрал предыдущую неделю
    elif message.payload.startswith('{"cmd":"back_diary_for_day_'):
        week = get_back_week()
        day = int(message.payload[27:-2])
    # Если пользователь выбрал следующую неделю
    elif message.payload.startswith('{"cmd":"next_diary_for_day_'):    
        week = get_next_week()
        day = int(message.payload[27:-2])
    
    try:
        diary = await get_diary( # Получаем дневник
            student.login,
            student.password,
            week,
            student.school,
            student.link,
            student.studentId
        )
        logging.info(f'{message.peer_id}: Get diary from NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return

    for lesson in diary['weekDays'][day]['lessons']:
        marks = ''
        homework_sgo = ''
        homework_db = ''

        if get_homework(lesson['subjectName'], student.school, student.clas):
            homework_db = get_homework(lesson['subjectName'], student.school, student.clas).homework

        if 'assignments' in lesson:
            for i in lesson['assignments']:
                #Если оценка не равна пустоте, то записываем ее
                if 'mark' in i:
                    marks += str(i['mark']['mark']) + ' '

                #Если тип задание = дз, то записываем
                if i['typeId'] == 3:
                    homework_sgo = i['assignmentName']
                else:
                    # ЕСли нет дз:
                    if homework_sgo == '':
                        homework_sgo = 'не задано'

        await message.answer(f"""
📚Предмет: {lesson['subjectName']}
🔎Кабинет: {lesson['room']}
📅Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
💬Домашние задание из СГО: {homework_sgo}
💬Последнее д/з из базы Бота (обновляли сами ученики): {homework_db}
💢Оценка: {marks}
        """)
        logging.info(f'{message.peer_id}: Send lesson information')








@bp.on.chat_message(PayloadStarts=['{"cmd":"next_diary_for_day', 
    '{"cmd":"back_diary_for_day', 
    '{"cmd":"diary_for_day'])
async def chat_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    chat_id = message.chat_id
    chat = get_chat_by_vk_id(chat_id)

    # Если пользователь выбрал текущую неделю
    if message.payload.startswith('{"cmd":"diary_for_day_'):
        week = get_week()
        day = int(message.payload[22:-2])
    # Если пользователь выбрал предыдущую неделю
    elif message.payload.startswith('{"cmd":"back_diary_for_day_'):
        week = get_back_week()
        day = int(message.payload[27:-2])
    # Если пользователь выбрал следующую неделю
    elif message.payload.startswith('{"cmd":"next_diary_for_day_'):    
        week = get_next_week()
        day = int(message.payload[27:-2])
    
    try:
        diary = await get_diary(
            chat.login,
            chat.password,
            week,
            chat.school,
            chat.link,
            chat.studentId
        )
        logging.info(f'{message.peer_id}: Get diary from NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return


    for lesson in diary['weekDays'][day]['lessons']:
        marks = ''
        homework_sgo = ''
        homework_db = ''
        
        if get_homework(lesson['subjectName'], chat.school, chat.clas):
            homework_db = get_homework(lesson['subjectName'], chat.school, chat.clas).homework

        if 'assignments' in lesson:
            for i in lesson['assignments']:
                #Если оценка не равна пустоте, то записываем ее
                if 'mark' in i:
                    marks += str(i['mark']['mark']) + ' '

                #Если тип задание = дз, то записываем
                if i['typeId'] == 3:
                    homework_sgo = i['assignmentName']
                else:
                    # ЕСли нет дз:
                    if homework_sgo == '':
                        homework_sgo = 'не задано'

        await message.answer(f"""
📚Предмет: {lesson['subjectName']}
🔎Кабинет: {lesson['room']}
📅Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
💬Домашние задание из СГО: {homework_sgo}
💬Последнее д/з из базы Бота (обновляли сами ученики): {homework_db}
💢Оценка: {marks}
        """)
        logging.info(f'{message.peer_id}: Send lesson information')