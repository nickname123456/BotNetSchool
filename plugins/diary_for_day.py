from ns import get_back_period, get_next_period
from ns import get_period
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_diary
import netschoolapi
from settings import admin_login, admin_password, admin_link, admin_school


bp = Blueprint('diary_for_day')
db = SQLighter('database.db')


@bp.on.private_message(payload=[{'cmd': 'diary_for_day'},
                        {'cmd': 'back_diary_for_day'},
                        {'cmd': 'next_diary_for_day'}])
async def diary_for_day(message: Message):
    userInfo = await bp.api.users.get(message.from_id)

    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не вошел в систему. Напиши "Вход"\n Или у тебя неверный логин/пароль')
        return

    keyboard = (
        Keyboard()
    )


    if message.payload == '{"cmd":"diary_for_day"}':
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_period(),
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id)
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            return
    
    elif message.payload == '{"cmd":"back_diary_for_day"}':
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_back_period(),
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id)
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            return

    elif message.payload == '{"cmd":"next_diary_for_day"}':    
        try:
            diary = await get_diary(
                db.get_account_login(userInfo[0].id),
                db.get_account_password(userInfo[0].id),
                get_next_period(),
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id)
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
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

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Если сообщение содержит

    #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
    db.edit_account_day(userInfo[0].id, day)
    db.commit()

    
    #Добавляем кнопку с содержанием номера урока, названия урока, оценки
    for lesson in diary.schedule[day].lessons:
        for assignment in lesson.assignments:
            if assignment.mark != None:
                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()
                break
            else:
                if assignment == lesson.assignments[0] and len(lesson.assignments) > 1:
                    continue
                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject,
                                {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()

        if len(lesson.assignments) == 0:
            numberOfTimes += 1
            keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject,
                            {'cmd': f'lesson_information_{numberOfTimes}'}))
            keyboard.row()

    keyboard.add(
        Text("Назад", {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer('Нажми на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)








@bp.on.chat_message(payload=[{'cmd': 'diary_for_day'},
                        {'cmd': 'back_diary_for_day'},
                        {'cmd': 'next_diary_for_day'}])
async def diary_for_day(message: Message):
    userInfo = await bp.api.users.get(message.from_id)


    keyboard = (
        Keyboard()
    )


    if message.payload == '{"cmd":"diary_for_day"}':
        period = ''
        try:
            diary = await get_diary(
                admin_login,
                admin_password,
                get_period(),
                admin_school,
                admin_link
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            return
    
    elif message.payload == '{"cmd":"back_diary_for_day"}':
        period = 'back_'
        try:
            diary = await get_diary(
                admin_login,
                admin_password,
                get_back_period(),
                admin_school,
                admin_link
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
            return

    elif message.payload == '{"cmd":"next_diary_for_day"}':
        period = 'next_'
        try:
            diary = await get_diary(
                admin_login,
                admin_password,
                get_next_period(),
                admin_school,
                admin_link
            )
        except netschoolapi.errors.AuthError:
            await message.answer('Неправильный логин или пароль!')
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

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Если сообщение содержит

    #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
    db.edit_account_day(userInfo[0].id, day)
    db.commit()

    
    #Добавляем кнопку с содержанием номера урока, названия урока, оценки
    for lesson in diary.schedule[day].lessons:
        for assignment in lesson.assignments:
            if assignment.mark != None:
                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'{period}lesson_information_{numberOfTimes}'}))
                keyboard.row()
                break
            else:
                if assignment == lesson.assignments[0] and len(lesson.assignments) > 1:
                    continue
                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject,
                                {'cmd': f'{period}lesson_information_{numberOfTimes}'}))
                keyboard.row()

        if len(lesson.assignments) == 0:
            numberOfTimes += 1
            keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject,
                            {'cmd': f'{period}lesson_information_{numberOfTimes}'}))
            keyboard.row()

    keyboard.add(
        Text("Назад", {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer('Нажми на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)