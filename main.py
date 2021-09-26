import asyncio
from netschoolapi import NetSchoolAPI
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD
import sqlite3

from vkbottle.tools.dev_tools import keyboard
from vkbottle.tools.dev_tools.keyboard.action import Payload


bot = Bot(token="фиг вам, а не токен!")


ns = NetSchoolAPI('https://sgo.edu-74.ru')
school = 'МАОУ "СОШ № 47 г. Челябинска"'


db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        id INT,
        login TEXT,
        password TEXT,
        isFirstLogin BIT
)""")
db.commit()



@bot.on.message(text="Меню")
@bot.on.message(payload={'cmd': 'menu'})
async def test(message: Message):
    keyboard = (
        Keyboard()
        .add(Text('Войти', {'cmd': 'login'}), color = KeyboardButtonColor.POSITIVE)
        .add(Text('Расписание на неделю', {'cmd': 'schedule'}), color = KeyboardButtonColor.PRIMARY)
    )

    await message.answer('Менюшка', keyboard=keyboard)




@bot.on.message(text=["вход <userLogin> <userPassword>", "вход"])
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
        cursor.execute('INSERT INTO students VALUES (?,?,?,?)', (userInfo[0].id, userLogin, userPassword, 1))
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

    global diary
    diary = await ns.diary()
    print(diary.schedule[0].lessons[0])

    



@bot.on.message(text="Расписание")
@bot.on.message(payload={'cmd': 'schedule'})
async def schedule(message: Message):

    keyboard=(
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    lessons =''
    for day in diary.schedule:
        for lesson in day.lessons:
            lessons += lesson.subject + '\n'
        lessons += '\n\n'
    await message.answer(lessons, keyboard=keyboard)






"""
@bot.on.chat_message()
async def echo(message: Message):
    await message.answer(message.text)
"""


bot.run_forever()
