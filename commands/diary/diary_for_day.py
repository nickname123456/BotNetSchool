from ns import get_back_week, get_next_week, get_week, get_diary
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message
from PostgreSQLighter import db
import netschoolapi
import logging
from VKRules import PayloadStarts


bp = Blueprint('diary_for_day') # Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts


@bp.on.private_message(PayloadStarts=['{"cmd":"next_diary_for_day', 
    '{"cmd":"back_diary_for_day', 
    '{"cmd":"diary_for_day'])
async def private_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    userId = message.from_id # ID юзера

    # Если у человека не правильный логин/пароль
    if db.get_account_correctData(userId) != 1:
        await message.answer('❌Вы не зарегистрированы! \n🤔Напишите "Начать" \n❌Или у вас неверный логин/пароль')
        logging.info(f'{message.peer_id}: User not found in db')
        return

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
            db.get_account_login(userId),
            db.get_account_password(userId),
            week,
            db.get_account_school(userId),
            db.get_account_link(userId),
            db.get_account_studentId(userId)
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
        try:
            homework_db = db.get_homework(
                db.get_account_school(userId),
                db.get_account_class(userId),
                lesson['subjectName']
            )
        except: pass

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
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            week,
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_studentId(chat_id)
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
        try:
            homework_db = db.get_homework(
                db.get_account_school(chat_id),
                db.get_account_class(chat_id),
                lesson['subjectName']
            )
        except: pass

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