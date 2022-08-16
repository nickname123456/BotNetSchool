from ns import get_back_week, get_next_week, get_week, get_diary
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts



bp = Blueprint('diary_for_day')# Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts


@bp.on.private_message(PayloadStarts=['{"cmd":"lesson_information_',
    '{"cmd":"next_lesson_information_',
    '{"cmd":"back_lesson_information_'])
async def private_lesson_information(message: Message):
    logging.info(f'{message.peer_id}: I get lesson information')
    userId = message.from_id # ID юзера

    day = db.get_account_day(userId) # Получаем день, на котором юзер

    # Если пользователь выбрал предыдущую неделю
    if 'back_' in message.payload:
        week = get_back_week()
        lesson = message.payload[32:-2]

    # Если пользователь выбрал следующую неделю
    elif 'next_' in message.payload:
        week = get_next_week()
        lesson = message.payload[32:-2]

    # Если пользователь выбрал текущую неделю
    else:
        week = get_week()
        lesson = message.payload[27:-2]
    
    db.edit_account_lesson(userId, lesson) # Редактируем номер урока, на котором юзер
    db.commit()
    
    diary = await get_diary( # Получаем дневник
        db.get_account_login(userId),
        db.get_account_password(userId),
        week,
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId))
    logging.info(f'{message.peer_id}: Get diary')
    
    lesson = diary['weekDays'][day]['lessons'][int(lesson)] # Получаем урок

    marks = ''
    homework = ''

    if 'assignments' in lesson:
        for i in lesson['assignments']:
            #Если оценка не равна пустоте, то записываем ее
            if 'mark' in i:
                marks += str(i['mark']['mark']) + ' '

            #Если тип задание = дз, то записываем
            if i['typeId'] == 3:
                homework = i['assignmentName']
            else:
                # ЕСли нет дз:
                if homework == '':
                    homework = 'не задано'

    await message.answer(f"""
📚Предмет: {lesson['subjectName']}
🔎Кабинет: {lesson['room']}
📅Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
💬Домашние задание: {homework}
💢Оценка: {marks}
    """)
    logging.info(f'{message.peer_id}: Send lesson information')






@bp.on.chat_message(PayloadStarts=['{"cmd":"lesson_information_',
    '{"cmd":"next_lesson_information_',
    '{"cmd":"back_lesson_information_'])
async def chat_lesson_information(message: Message):
    logging.info(f'{message.peer_id}: I get lesson information')
    chat_id = message.chat_id

    day = db.get_chat_day(chat_id) # Получаем день, на котором юзер

    # Если пользователь выбрал предыдущую неделю
    if 'back_' in message.payload:
        week = get_back_week()
        lesson = message.payload[32:-2]

    # Если пользователь выбрал следующую неделю
    elif 'next_' in message.payload:
        week = get_next_week()
        lesson = message.payload[32:-2]

    # Если пользователь выбрал текущую неделю
    else:
        week = get_week()
        lesson = message.payload[27:-2]
    
    db.edit_chat_lesson(chat_id, lesson) # Редактируем номер урока, на котором юзер
    db.commit()
    
    diary = await get_diary(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        week,
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id))
    logging.info(f'{message.peer_id}: Get diary')
    
    lesson = diary['weekDays'][day]['lessons'][int(lesson)]

    marks = ''
    homework = ''

    if 'assignments' in lesson:
        for i in lesson['assignments']:
            #Если оценка не равна пустоте, то записываем ее
            if 'mark' in i:
                marks += str(i['mark']['mark']) + ' '

            #Если тип задание = дз, то записываем
            if i['typeId'] == 3:
                homework = i['assignmentName']
            else:
                # ЕСли нет дз:
                if homework == '':
                    homework = 'не задано'

    await message.answer(f"""
📚Предмет: {lesson['subjectName']}
🔎Кабинет: {lesson['room']}
📅Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
💬Домашние задание: {homework}
💢Оценка: {marks}
    """)
    logging.info(f'{message.peer_id}: Send lesson information')