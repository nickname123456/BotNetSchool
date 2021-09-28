import asyncio
import json
from netschoolapi import NetSchoolAPI
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD
import sqlite3

from vkbottle.tools.dev_tools import keyboard
from vkbottle.tools.dev_tools.keyboard.action import Payload


#Входим в группу
bot = Bot(token="19ce7bdfe981c0498b7e4e0ebc2118367182fc4d9859869a89167b534481d9e55615b906f208aa3ba7729")


#Список дневников учеников
diarys = {}

ns = NetSchoolAPI('https://sgo.edu-74.ru')
school = 'МАОУ "СОШ № 47 г. Челябинска"'


#Создаем нашу бд
db = sqlite3.connect('database.db')
cursor = db.cursor()

#СОЗДАТЬ ТАБЛИЦУ, ЕСЛИ ОНА НЕ СУЩЕСТВЕТ
cursor.execute("""CREATE TABLE IF NOT EXISTS students ( 
        id INT,
        login TEXT,
        password TEXT,
        isFirstLogin BIT,
        day INT,
        lesson INT
)""")
#Сохраняем изменения бд
db.commit()


print('')
print('-------------------------------')
print('  Скрипт Сетевого Города запущен.')
print('  Разработчик: Кирилл Арзамасцев ')
print('  https://vk.com/kirillarz')

print('-------------------------------')
print('')



try:
    #Если написали "Меню" или нажали на соответствующую кнопку
    @bot.on.message(text="Меню")
    @bot.on.message(payload={'cmd': 'menu'})
    async def menu(message: Message):
        #Создаем клавиатуру
        keyboard = (
            Keyboard()
            #Добавить кнопки
            .add(Text('Войти', {'cmd': 'login'}), color = KeyboardButtonColor.POSITIVE)
            .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.PRIMARY)
        )

        #Ответ в чат
        await message.answer('Ты в главном меню.', keyboard=keyboard)



    #Если написали "Вход" или нажали на соответствующую кнопку
    @bot.on.message(text=["Вход <userLogin> <userPassword>", "Вход"])
    @bot.on.message(payload={'cmd': 'login'})
    async def login(message: Message, userLogin = None, userPassword = None):
        #Собираем инфу о пользователе
        userInfo = await bot.api.users.get(message.from_id)

        #Выбрать isFirstLogin ИЗ ТАБЛИЦЫ ГДЕ айди РАВЕН айди отправителя
        cursor.execute(f"SELECT isFirstLogin FROM students WHERE id = '{userInfo[0].id}'")
        #Если человека нет в бд (переменная пуста)
        if cursor.fetchone() is None:

            #Если не введены пароль и логин
            if userLogin == None and userPassword == None:
                await message.answer("Так... Смотрю тебя теще нет в моей бд. Но ничего страшного сейчас все будет!")
                await message.answer('Напиши "вход <твой логин> <пароль>"')
                return
            
        #Если пароль и логин введены
        if userLogin != None and userPassword != None:
            #Записать их в бд
            cursor.execute('INSERT INTO students VALUES (?,?,?,?,?,?)', (userInfo[0].id, userLogin, userPassword, 1, 0, 0))
            db.commit()

        #ВЫБРАТЬ логин ИЗ ТАБЛИЦЫ ГДЕ айди РАВЕН айди отправителя
        cursor.execute(f"SELECT login FROM students WHERE id = '{userInfo[0].id}'")
        #Записываем логин из бд в переменную
        userLogin = cursor.fetchone()[0]
        print(userLogin)

        cursor.execute(f"SELECT password FROM students WHERE id = '{userInfo[0].id}'")
        userPassword = cursor.fetchone()[0]
        print(userPassword)

        #Авторезируемся в Сетевом Городе
        await ns.login(
            userLogin,
            userPassword,
            school,
        )

        #Дневник ученика равен дневнику из СГ
        diarys[userInfo[0].id] = await ns.diary()
        await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {userLogin}')
        #Выходим из СГ
        await ns.logout()


        #Спустя 10 минут удаляем из памяти дневник ученика
        await asyncio.sleep(600)
        diarys.pop(userInfo[0].id)
        await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')

        



    @bot.on.message(payload={'cmd': 'keyboard_schedule'})
    async def keyboard_schedule(message: Message):

        keyboard = (
            Keyboard()
            #Добавить кнопку
            .add(Text('Понедельник', {"cmd": "schedule_for_day"}))
            #Начать с новой строки
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

        #Если дневника нет в списке
        if userInfo[0].id not in diarys:
            await message.answer('Ты не вошел в систему. Напиши "Вход"')
            return

        keyboard = (
            Keyboard()
        )

        #Число, нужное для запоминания, какой урок будет выбран
        numberOfTimes = -1
        #Если сообщение содержит
        if 'Понедельник' in message.text:

            #ОБНОВИТЬ ТАБЛИЦУ students ЗАДАТЬ ПЕРЕМЕННОЙ day ЗНАЧЕНИЕ 0 ГДЕ айди РАВЕН айди ОТПРАВИТЕЛЯ
            cursor.execute(f'UPDATE students SET day = {0} WHERE id = "{userInfo[0].id}"')
            db.commit()

            #Добавляем кнопку с содержанием номера урока, названия урока, оценки
            for lesson in diarys[userInfo[0].id].schedule[0].lessons:
                for assignment in lesson.assignments:
                    if assignment.mark != None:
                        numberOfTimes +=1
                        keyboard.add(Text(str(numberOfTimes + 1) + '. ' + lesson.subject +
                                    ' ' + str(assignment.mark), {'cmd': f'lesson_information_{numberOfTimes}'}))
                        keyboard.row()
                        break

                    else:
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

                    else:
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

                    else:
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

                    else:
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

                    else:
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
        homework = ''

        for i in lesson.assignments:
            #Если оценка не равна пустоте, то записываем ее
            if i.mark != None:
                marks += str(i.mark) + ' '

            #Если тип задание = дз, то записываем
            if i.type == 'Домашнее задание':
                homework = i.content
                pass
            else:
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


        




    bot.run_forever()

except Exception as e:
    print(e.message, e.args)
