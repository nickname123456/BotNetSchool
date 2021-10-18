from ns import get_back_period, get_next_period
from ns import get_period
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_diary
import netschoolapi


bp = Blueprint('diary_for_day')
db = SQLighter('database.db')


@bp.on.message(payload={'cmd': 'diary_for_day'})
async def diary_for_day(message: Message):
    userInfo = await bp.api.users.get(message.from_id)

    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не вошел в систему. Напиши "Вход"\n Или у тебя неверный логин/пароль')
        return

    keyboard = (
        Keyboard()
    )

    try:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_period()
            
        )
    except netschoolapi.errors.AuthError:
        await message.answer('Неправильный логин или пароль!')
        return

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Если сообщение содержит
    if 'Понедельник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 0)
        db.commit()

        
        #Добавляем кнопку с содержанием номера урока, названия урока, оценки
        for lesson in diary.schedule[0].lessons:
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

    if 'Вторник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 1)
        db.commit()

        for lesson in diary.schedule[1].lessons:
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

    if 'Среда' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 2)
        db.commit()


        for lesson in diary.schedule[2].lessons:
            for assignment in lesson.assignments:
                if assignment.mark != None:
                    numberOfTimes += 1
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject + ' ' + str(
                        assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
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

    if 'Четверг' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 3)
        db.commit()

        for lesson in diary.schedule[3].lessons:
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

    if 'Пятница' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 4)
        db.commit()

        for lesson in diary.schedule[4].lessons:
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







@bp.on.message(payload={'cmd': 'next_diary_for_day'})
async def diary_for_day(message: Message):
    userInfo = await bp.api.users.get(message.from_id)

    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не вошел в систему. Напиши "Вход"\n Или у тебя неверный логин/пароль')
        return

    keyboard = (
        Keyboard()
    )

    try:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_next_period()
            
        )
    except netschoolapi.errors.AuthError:
        await message.answer('Неправильный логин или пароль!')
        return

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Если сообщение содержит
    if 'Понедельник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 0)
        db.commit()

        
        #Добавляем кнопку с содержанием номера урока, названия урока, оценки
        for lesson in diary.schedule[0].lessons:
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

    if 'Вторник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 1)
        db.commit()

        for lesson in diary.schedule[1].lessons:
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

    if 'Среда' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 2)
        db.commit()


        for lesson in diary.schedule[2].lessons:
            for assignment in lesson.assignments:
                if assignment.mark != None:
                    numberOfTimes += 1
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject + ' ' + str(
                        assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
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

    if 'Четверг' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 3)
        db.commit()

        for lesson in diary.schedule[3].lessons:
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

    if 'Пятница' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 4)
        db.commit()

        for lesson in diary.schedule[4].lessons:
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




@bp.on.message(payload={'cmd': 'back_diary_for_day'})
async def diary_for_day(message: Message):
    userInfo = await bp.api.users.get(message.from_id)

    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не вошел в систему. Напиши "Вход"\n Или у тебя неверный логин/пароль')
        return

    keyboard = (
        Keyboard()
    )

    try:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_back_period()
            
        )
    except netschoolapi.errors.AuthError:
        await message.answer('Неправильный логин или пароль!')
        return

    #Число, нужное для запоминания, какой урок будет выбран
    numberOfTimes = -1
    #Если сообщение содержит
    if 'Понедельник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 0)
        db.commit()

        
        #Добавляем кнопку с содержанием номера урока, названия урока, оценки
        for lesson in diary.schedule[0].lessons:
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

    if 'Вторник' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 1)
        db.commit()

        for lesson in diary.schedule[1].lessons:
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

    if 'Среда' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 2)
        db.commit()


        for lesson in diary.schedule[2].lessons:
            for assignment in lesson.assignments:
                if assignment.mark != None:
                    numberOfTimes += 1
                    keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject + ' ' + str(
                        assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
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

    if 'Четверг' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 3)
        db.commit()

        for lesson in diary.schedule[3].lessons:
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

    if 'Пятница' in message.text:

        #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
        db.edit_account_day(userInfo[0].id, 4)
        db.commit()

        for lesson in diary.schedule[4].lessons:
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




