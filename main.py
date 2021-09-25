import asyncio
from netschoolapi import NetSchoolAPI
from vkbottle.bot import Bot, Message
import sqlite3


bot = Bot(token="19ce7bdfe981c0498b7e4e0ebc2118367182fc4d9859869a89167b534481d9e55615b906f208aa3ba7729")


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




@bot.on.message(text=["вход <userLogin> <userPassword>", "вход"])
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

    diary = await ns.diary()
    print(diary.schedule[0].lessons[0])
    




"""
@bot.on.chat_message()
async def echo(message: Message):
    await message.answer(message.text)
"""


bot.run_forever()
