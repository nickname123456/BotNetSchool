from ns import get_back_week, get_next_week, get_week, get_diary
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts



bp = Blueprint('diary_for_day')# Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts


@bp.on.private_message(PayloadStarts='{"cmd":"lesson_information_')
async def private_lesson_information(message: Message):
    logging.info(f'{message.peer_id}: I get lesson information')
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере

    db.edit_account_lesson(userInfo[0].id, message.payload[27::29]) # Редактируем номер урока, на котором юзер
    db.commit()

    day = db.get_account_day(userInfo[0].id) # Получаем день, на котором юзер

    # Если пользователь выбрал предыдущую неделю
    if 'back_' in message.payload:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_back_week(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id),
            db.get_account_studentId(userInfo[0].id))
        logging.info(f'{message.peer_id}: Get back diary')

        lesson = diary['weekDays'][day]['lessons'][int(message.payload[32::34])]

    # Если пользователь выбрал следующую неделю
    elif 'next_' in message.payload:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_next_week(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id),
            db.get_account_studentId(userInfo[0].id)) 
        logging.info(f'{message.peer_id}: Get next diary')
        
        lesson = diary['weekDays'][day]['lessons'][int(message.payload[32::34])]

    # Если пользователь выбрал текущую неделю
    else:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_week(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id),
            db.get_account_studentId(userInfo[0].id))
        logging.info(f'{message.peer_id}: Get diary')
        
        lesson = diary['weekDays'][day]['lessons'][int(message.payload[27::29])]

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
Предмет: {lesson['subjectName']}
Кабинет: {lesson['room']}
Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
Домашние задание: {homework}
Оценка: {marks}
    """)
    logging.info(f'{message.peer_id}: Send lesson information')






@bp.on.chat_message(PayloadStarts='{"cmd":"lesson_information_')
async def chat_lesson_information(message: Message):
    logging.info(f'{message.peer_id}: I get lesson information from chat')
    chat_id = message.chat_id # Чат айди

    try:
        day = db.get_chat_day(chat_id)
    # Если чата нет в бд
    except:
        logging.info(f'{message.peer_id}: Not found chat in db')
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return


    try:
        # Если пользователь выбрал предыдущую неделю
        if 'back_' in message.payload:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_back_week(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            logging.info(f'{message.peer_id}: Get back diary')

            lesson = diary['weekDays'][day]['lessons'][int(message.payload[32::34])]

        # Если пользователь выбрал следующую неделю
        elif 'next_' in message.payload:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_next_week(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            logging.info(f'{message.peer_id}: Get next diary')
            
            lesson = diary['weekDays'][day]['lessons'][int(message.payload[32::34])]

        # Если пользователь выбрал текущую неделю
        else:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_week(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            logging.info(f'{message.peer_id}: Get diary')
            
            lesson = diary['weekDays'][day]['lessons'][int(message.payload[27::29])]
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return

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
Предмет: {lesson['subjectName']}
Кабинет: {lesson['room']}
Время проведения урока: {lesson['startTime']} - {lesson['endTime']}
Домашние задание: {homework}
Оценка: {marks}
    """)
    logging.info(f'{message.peer_id}: Send lesson information')