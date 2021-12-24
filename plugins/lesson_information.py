from ns import get_back_period, get_next_period, get_period, get_diary
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter



bp = Blueprint('diary_for_day')# Объявляем команду
db = SQLighter('database.db')# Подключаемся к базе данных







@bp.on.private_message(payload=[{'cmd': 'lesson_information_0'},
                        {'cmd': 'lesson_information_1'},
                        {'cmd': 'lesson_information_2'},
                        {'cmd': 'lesson_information_3'},
                        {'cmd': 'lesson_information_4'},
                        {'cmd': 'lesson_information_5'},
                        {'cmd': 'lesson_information_6'},
                        {'cmd': 'lesson_information_7'},
                        {'cmd': 'back_lesson_information_0'},
                        {'cmd': 'back_lesson_information_1'},
                        {'cmd': 'back_lesson_information_2'},
                        {'cmd': 'back_lesson_information_3'},
                        {'cmd': 'back_lesson_information_4'},
                        {'cmd': 'back_lesson_information_5'},
                        {'cmd': 'back_lesson_information_6'},
                        {'cmd': 'back_lesson_information_7'},
                        {'cmd': 'next_lesson_information_0'},
                        {'cmd': 'next_lesson_information_1'},
                        {'cmd': 'next_lesson_information_2'},
                        {'cmd': 'next_lesson_information_3'},
                        {'cmd': 'next_lesson_information_4'},
                        {'cmd': 'next_lesson_information_5'},
                        {'cmd': 'next_lesson_information_6'},
                        {'cmd': 'next_lesson_information_7'}])
async def lesson_information(message: Message):
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере

    db.edit_account_lesson(userInfo[0].id, message.payload[27::29]) # Редактируем номер урока, на котором юзер
    db.commit()

    day = db.get_account_day(userInfo[0].id) # Получаем день, на котором юзер

    # Если пользователь выбрал предыдущую неделю
    if 'back_' in message.payload:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_back_period(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id))

        lesson = diary.schedule[day].lessons[int(message.payload[32::34])]

    # Если пользователь выбрал следующую неделю
    elif 'next_' in message.payload:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_next_period(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id)) 
        
        lesson = diary.schedule[day].lessons[int(message.payload[32::34])]

    # Если пользователь выбрал текущую неделю
    else:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_period(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id))
        
        lesson = diary.schedule[day].lessons[int(message.payload[27::29])]
        


    marks = ''
    homework = ''

    for i in lesson.assignments:
        #Если оценка не равна пустоте, то записываем ее
        if i.mark != None:
            marks += str(i.mark) + ' '

        #Если тип задание = дз, то записываем
        if i.type == 'Домашнее задание':
            homework = i.content
        else:
            # ЕСли нет дз:
            if homework == '':
                homework = 'не задано'

    #print(lesson.subject)
    #print(lesson.room)
    #print(f'{lesson.start:%H, %M} - {lesson.end:%H.%M}')
    #print(lesson.assignments)
    #print(lesson.assignments[0].content)
    #print(marks)

    await message.answer(f"""
Предмет: {lesson.subject}
Кабинет: {lesson.room}
Время проведения урока: {lesson.start:%H.%M} - {lesson.end:%H.%M}
Домашние задание: {homework}
Оценка: {marks}
    """)






@bp.on.chat_message(payload=[{'cmd': 'lesson_information_0'},
                        {'cmd': 'lesson_information_1'},
                        {'cmd': 'lesson_information_2'},
                        {'cmd': 'lesson_information_3'},
                        {'cmd': 'lesson_information_4'},
                        {'cmd': 'lesson_information_5'},
                        {'cmd': 'lesson_information_6'},
                        {'cmd': 'lesson_information_7'},
                        {'cmd': 'back_lesson_information_0'},
                        {'cmd': 'back_lesson_information_1'},
                        {'cmd': 'back_lesson_information_2'},
                        {'cmd': 'back_lesson_information_3'},
                        {'cmd': 'back_lesson_information_4'},
                        {'cmd': 'back_lesson_information_5'},
                        {'cmd': 'back_lesson_information_6'},
                        {'cmd': 'back_lesson_information_7'},
                        {'cmd': 'next_lesson_information_0'},
                        {'cmd': 'next_lesson_information_1'},
                        {'cmd': 'next_lesson_information_2'},
                        {'cmd': 'next_lesson_information_3'},
                        {'cmd': 'next_lesson_information_4'},
                        {'cmd': 'next_lesson_information_5'},
                        {'cmd': 'next_lesson_information_6'},
                        {'cmd': 'next_lesson_information_7'}])
async def lesson_information(message: Message):
    chat_id = message.chat_id # Чат айди

    try:
        day = db.get_chat_day(chat_id)
    # Если чата нет в бд
    except:
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return


    try:
        # Если пользователь выбрал предыдущую неделю
        if 'back_' in message.payload:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_back_period(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id))

            lesson = diary.schedule[day].lessons[int(message.payload[32::34])]

        # Если пользователь выбрал следующую неделю
        elif 'next_' in message.payload:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_next_period(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id))
            
            lesson = diary.schedule[day].lessons[int(message.payload[32::34])]

        # Если пользователь выбрал текущую неделю
        else:
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_period(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id))
            
            lesson = diary.schedule[day].lessons[int(message.payload[27::29])]
    except:
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return
        


    marks = ''
    homework = ''

    for i in lesson.assignments:
        #Если оценка не равна пустоте, то записываем ее
        if i.mark != None:
            marks += str(i.mark) + ' '

        #Если тип задание = дз, то записываем
        if i.type == 'Домашнее задание':
            homework = i.content
        # ЕСли нет дз:
        else:
            if homework == '':
                homework = 'не задано'

    #print(lesson.subject)
    #print(lesson.room)
    #print(f'{lesson.start:%H, %M} - {lesson.end:%H.%M}')
    #print(lesson.assignments)
    #print(lesson.assignments[0].content)
    #print(marks)

    await message.answer(f"""
Предмет: {lesson.subject}
Кабинет: {lesson.room}
Время проведения урока: {lesson.start:%H.%M} - {lesson.end:%H.%M}
Домашние задание: {homework}
    """)