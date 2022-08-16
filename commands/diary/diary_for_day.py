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

    # Создаем клавиатуру
    keyboard = (
        Keyboard()
    )

    # Если пользователь выбрал текущую неделю
    if message.payload.startswith('{"cmd":"diary_for_day_'):
        week = get_week()
        period_in_payload = ''
        day = int(message.payload[22:-2])
    # Если пользователь выбрал предыдущую неделю
    elif message.payload.startswith('{"cmd":"back_diary_for_day_'):
        week = get_back_week()
        period_in_payload = 'back_'
        day = int(message.payload[27:-2])
    # Если пользователь выбрал следующую неделю
    elif message.payload.startswith('{"cmd":"next_diary_for_day_'):    
        week = get_next_week()
        period_in_payload = 'next_'
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

    # Меняем данные о дне в бд
    db.edit_account_day(userId, day)
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
    await message.answer('👆Нажмите на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Send keyboard for day')








@bp.on.chat_message(PayloadStarts=['{"cmd":"next_diary_for_day', 
    '{"cmd":"back_diary_for_day', 
    '{"cmd":"diary_for_day'])
async def chat_diary_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get diary for day')
    chat_id = message.chat_id

    # Создаем клавиатуру
    keyboard = (
        Keyboard()
    )

    # Если пользователь выбрал текущую неделю
    if message.payload.startswith('{"cmd":"diary_for_day_'):
        week = get_week()
        period_in_payload = ''
        day = int(message.payload[22:-2])
    # Если пользователь выбрал предыдущую неделю
    elif message.payload.startswith('{"cmd":"back_diary_for_day_'):
        week = get_back_week()
        period_in_payload = 'back_'
        day = int(message.payload[27:-2])
    # Если пользователь выбрал следующую неделю
    elif message.payload.startswith('{"cmd":"next_diary_for_day_'):    
        week = get_next_week()
        period_in_payload = 'next_'
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
    await message.answer('👆Нажмите на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Send keyboard for day')