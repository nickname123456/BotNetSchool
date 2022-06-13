from ns import get_back_week, get_next_week
from ns import get_week
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
from ns import get_diary
import netschoolapi
import logging


bp = Blueprint('diary_for_day') # Объявляем команду


@bp.on.private_message(payload=[{'cmd': 'diary_for_day'},
                                {'cmd': 'back_diary_for_day'},
                                {'cmd': 'next_diary_for_day'}])
async def private_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере

    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        logging.info(f'{message.peer_id}: User not found in db')
        return

    # Создаем клавиатуру
    keyboard = (
        Keyboard()
    )

    # Если пользователь выбрал текущую неделю
    if message.payload == '{"cmd":"diary_for_day"}':
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_week(),
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id),
                db.get_account_studentId(userInfo[0].id)
            )
            period_in_payload = ''
            logging.info(f'{message.peer_id}: Get diary from NetSchool')
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            logging.info(f'{message.peer_id}: Incorrect login or password!')
            return
    
    # Если пользователь выбрал предыдущую неделю
    elif message.payload == '{"cmd":"back_diary_for_day"}':
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_back_week(), # Получить предыдущую неделю
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id),
                db.get_account_studentId(userInfo[0].id)
            )
            period_in_payload = 'back_'
            logging.info(f'{message.peer_id}: Get diary from NetSchool')
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            logging.info(f'{message.peer_id}: Incorrect login or password!')
            return

    # Если пользователь выбрал следующую неделю
    elif message.payload == '{"cmd":"next_diary_for_day"}':    
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_next_week(), # Получить следующую неделю
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id),
                db.get_account_studentId(userInfo[0].id)
            )
            period_in_payload = 'next_'
            logging.info(f'{message.peer_id}: Get diary from NetSchool')
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            logging.info(f'{message.peer_id}: Incorrect login or password!')
            return
    

    if 'Понедельник' in message.text:
        day = 0
    elif 'Вторник' in message.text:
        day = 1
    elif 'Среда' in message.text:
        day = 2
    elif 'Четверг' in message.text:
        day = 3
    elif 'Пятница' in message.text:
        day = 4
    # Меняем данные о дне в бд
    db.edit_account_day(userInfo[0].id, day)
    db.commit()

    
    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Добавляем кнопку с содержанием номера урока, названия урока, оценки
    for lesson in diary['weekDays'][day]['lessons']:
        if 'assignments' in lesson:
            for assignment in lesson['assignments']:
                if 'mark' in assignment: # Если есть оценка
                    numberOfTimes += 1
                    # Добавляем кнопку с уроком
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'] +
                                        ' ' + str(assignment['mark']['mark']), {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
                    keyboard.row()
                    break
                else: # Если нет оценки:
                    if assignment == lesson['assignments'][0] and len(lesson['assignments']) > 1: # Если помимо этого задания есть другое, то переходим к нему (например если задано дз, и была работа на уроке)
                        continue
                    # Добавляем кнопку с уроком
                    numberOfTimes += 1
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'],
                                    {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
                    keyboard.row()

        else: # Если заданий вообще нет:
            numberOfTimes += 1
            # Добавляем кнопку с уроком
            keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'],
                            {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
            keyboard.row()

    # Добавляем кнопку назад
    keyboard.add(
        Text("Назад", {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer('Нажми на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Send keyboard for day')








@bp.on.chat_message(payload=[{'cmd': 'diary_for_day'},
                        {'cmd': 'back_diary_for_day'},
                        {'cmd': 'next_diary_for_day'}])
async def chat_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    chat_id = message.chat_id

    # Создаем клавиатуру
    keyboard = (
        Keyboard()
    )


    try:
        # Если пользователь выбрал текущую неделю
        if message.payload == '{"cmd":"diary_for_day"}':
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_week(),
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            period_in_payload = ''
            logging.info(f'{message.peer_id}: Get diary from NetSchool')
            
        # Если пользователь выбрал предыдущую неделю
        elif message.payload == '{"cmd":"back_diary_for_day"}':
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_back_week(), # Получить предыдущую неделю
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            period_in_payload = 'back_'
            logging.info(f'{message.peer_id}: Get diary from NetSchool')

        # Если пользователь выбрал следующую неделю
        elif message.payload == '{"cmd":"next_diary_for_day"}':
            diary = await get_diary(
                db.get_chat_login(chat_id),
                db.get_chat_password(chat_id),
                get_next_week(), # Получить следующую неделю
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id),
                db.get_chat_studentId(chat_id))
            period_in_payload = 'next_'
            logging.info(f'{message.peer_id}: Get diary from NetSchool')
            
    except:
        logging.info(f'{message.peer_id}: Incorrect login or password or not linked chat!')
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return
    

    if 'Понедельник' in message.text:
        day = 0
    elif 'Вторник' in message.text:
        day = 1
    elif 'Среда' in message.text:
        day = 2
    elif 'Четверг' in message.text:
        day = 3
    elif 'Пятница' in message.text:
        day = 4
    # Меняем данные о дне в бд
    db.edit_chat_day(chat_id, day)
    db.commit()

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Добавляем кнопку с содержанием номера урока, названия урока, оценки
    for lesson in diary['weekDays'][day]['lessons']:
        if 'assignments' in lesson:
            for assignment in lesson['assignments']:
                if 'mark' in assignment: # Если есть оценка
                    numberOfTimes += 1
                    # Добавляем кнопку с уроком
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'] +
                                        ' ' + str(assignment['mark']['mark']), {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
                    keyboard.row()
                    break
                else: # Если нет оценки:
                    if assignment == lesson['assignments'][0] and len(lesson['assignments']) > 1: # Если помимо этого задания есть другое, то переходим к нему (например если задано дз, и была работа на уроке)
                        continue
                    # Добавляем кнопку с уроком
                    numberOfTimes += 1
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'],
                                    {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
                    keyboard.row()

        else: # Если заданий вообще нет:
            numberOfTimes += 1
            # Добавляем кнопку с уроком
            keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson['subjectName'],
                            {'cmd': f'{period_in_payload}lesson_information_{numberOfTimes}'}))
            keyboard.row()

    # Добавляем кнопку назад
    keyboard.add(
        Text("Назад", {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer('Нажми на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Send keyboard for day')