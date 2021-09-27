import asyncio
import json
from netschoolapi import NetSchoolAPI
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD
import sqlite3

from vkbottle.tools.dev_tools import keyboard
from vkbottle.tools.dev_tools.keyboard.action import Payload


bot = Bot(token="фиг вам")


diarys = {}
ns = NetSchoolAPI('https://sgo.edu-74.ru')
school = 'МАОУ "СОШ № 47 г. Челябинска"'


db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        id INT,
        login TEXT,
        password TEXT,
        isFirstLogin BIT,
        day INT,
        lesson INT
)""")
db.commit()


print('')
print('-------------------------------')
print('  Скрипт Сетевого Города запущен.')
print('  Разработчик: Кирилл Арзамасцев ')
print('  https://vk.com/kirillarz')

print('-------------------------------')
print('')



try:

    @bot.on.message(text="Меню")
    @bot.on.message(payload={'cmd': 'menu'})
    async def menu(message: Message):
        keyboard = (
            Keyboard()
            .add(Text('Войти', {'cmd': 'login'}), color = KeyboardButtonColor.POSITIVE)
            .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.PRIMARY)
        )

        await message.answer('Ты в главном меню.', keyboard=keyboard)




    @bot.on.message(text=["Вход <userLogin> <userPassword>", "Вход"])
    @bot.on.message(payload={'cmd': 'login'})
    async def login(message: Message, userLogin = None, userPassword = None):
        userInfo = await bot.api.users.get(message.from_id)

        cursor.execute(f"SELECT isFirstLogin FROM students WHERE id = '{userInfo[0].id}'")
        if cursor.fetchone() is None:

            if userLogin == None and userPassword == None:
                await message.answer("Так... Смотрю тебя теще нет в моей бд. Но ничего страшного сейчас все будет!")
                await message.answer('Напиши "вход <твой логин> <пароль>"')
                return
            
        if userLogin != None and userPassword != None:
            cursor.execute('INSERT INTO students VALUES (?,?,?,?,?,?)', (userInfo[0].id, userLogin, userPassword, 1, 0, 0))
            db.commit()

        cursor.execute(f"SELECT login FROM students WHERE id = '{userInfo[0].id}'")
        userLogin = cursor.fetchone()[0]
        print(userLogin)

        cursor.execute(f"SELECT password FROM students WHERE id = '{userInfo[0].id}'")
        userPassword = cursor.fetchone()[0]
        print(userPassword)

        await ns.login(
            userLogin,
            userPassword,
            school,
        )

        diarys[userInfo[0].id] = await ns.diary()
        await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {userLogin}')
        await ns.logout()


        await asyncio.sleep(600)
        diarys.pop(userInfo[0].id)
        await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')

        



    @bot.on.message(text="Расписание")
    @bot.on.message(payload={'cmd': 'keyboard_schedule'})
    async def keyboard_schedule(message: Message):

        keyboard = (
            Keyboard()
            .add(Text('Понедельник', {"cmd": "schedule_for_day"}))
            .row()
            .add(Text('Вторник', {'cmd': 'schedule_for_day'}))
            .row()
            .add(Text('Среда', {'cmd': 'schedule_for_day'}))
            .row()
            .add(Text('Четверг', {'cmd': 'schedule_for_day'}))
            .row()
            .add(Text('Пятница', {'cmd': 'schedule_for_day'}))
            .row()
            .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        )

        await message.answer('На какой день хочешь узнать расписание?', keyboard=keyboard)




    @bot.on.message(payload={'cmd': 'schedule_for_day'})
    async def schedule_for_day(message: Message):
        userInfo = await bot.api.users.get(message.from_id)

        if userInfo[0].id not in diarys:
            await message.answer('Ты не вошел в систему. Напиши "Вход"')
            return

        keyboard = (
            Keyboard()
        )

        numberOfTimes = -1
        if 'Понедельник' in message.text:

            cursor.execute(f'UPDATE students SET day = {0} WHERE id = "{userInfo[0].id}"')
            db.commit()

            for lesson in diarys[userInfo[0].id].schedule[0].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject, {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()

        
        if 'Вторник' in message.text:

            cursor.execute(f'UPDATE students SET day = {1} WHERE id = "{userInfo[0].id}"')
            db.commit()

            for lesson in diarys[userInfo[0].id].schedule[1].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject, {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()

        
        if 'Среда' in message.text:

            cursor.execute(f'UPDATE students SET day = {2} WHERE id = "{userInfo[0].id}"')
            db.commit()

            for lesson in diarys[userInfo[0].id].schedule[2].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject + ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject, {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()


        if 'Четверг' in message.text:

            cursor.execute(f'UPDATE students SET day = {3} WHERE id = "{userInfo[0].id}"')
            db.commit()

            for lesson in diarys[userInfo[0].id].schedule[3].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject, {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()


        if 'Пятница' in message.text:

            cursor.execute(f'UPDATE students SET day = {4} WHERE id = "{userInfo[0].id}"')
            db.commit()

            for lesson in diarys[userInfo[0].id].schedule[4].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                numberOfTimes += 1
                keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject, {'cmd': f'lesson_information_{numberOfTimes}'}))
                keyboard.row()






        keyboard.add(Text("Назад", {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer('Нажми на предмет для того, чтобы увидеть информацию о нем', keyboard=keyboard)


    @bot.on.message(payload=[{'cmd': 'lesson_information_0'},
                            {'cmd': 'lesson_information_1'},
                            {'cmd': 'lesson_information_2'},
                            {'cmd': 'lesson_information_3'},
                            {'cmd': 'lesson_information_4'},
                            {'cmd': 'lesson_information_5'},
                            {'cmd': 'lesson_information_6'},
                            {'cmd': 'lesson_information_7'}])
    async def lesson_information(message: Message):
        userInfo = await bot.api.users.get(message.from_id)

        cursor.execute(f'UPDATE students SET lesson = {message.payload[27::29]} WHERE id = "{userInfo[0].id}"')
        db.commit()

        cursor.execute(f"SELECT day FROM students WHERE id = '{userInfo[0].id}'")
        day = cursor.fetchone()[0]

        lesson = diarys[userInfo[0].id].schedule[day].lessons[int(message.payload[27::29])]

        marks = ''

        if len(lesson.assignments) > 0:
            homework = lesson.assignments[0].content
        else:
            homework = 'не задано'

        for assignment in lesson.assignments:
            if assignment.mark != None:
                marks += str(assignment.mark) + ' '

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


        




    bot.run_forever()

except Exception as e:
    print(e.message, e.args)
