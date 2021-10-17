from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from netschoolapi import NetSchoolAPI
from sqlighter import SQLighter


bp = Blueprint('login')
db = SQLighter('database.db')
ns = NetSchoolAPI('https://sgo.edu-74.ru')



#Если написали "Вход" или нажали на соответствующую кнопку
@bp.on.message(text=["Вход <userLogin> <userPassword>", "Вход"])
@bp.on.message(payload={'cmd': 'login'})
async def login(message: Message, userLogin=None, userPassword=None):
    #Собираем инфу о пользователе
    userInfo = await bp.api.users.get(message.from_id)

    
    if db.get_account_isFirstLogin(userInfo[0].id) is None:

        #Если не введены пароль и логин
        if userLogin == None and userPassword == None:
            await message.answer("Так... Смотрю тебя теще нет в моей бд. Но ничего страшного сейчас все будет!")
            await message.answer('Напиши "вход <твой логин> <пароль>"')
            return

        #Если пароль и логин введены
        if userLogin != None and userPassword != None:
            #Записать их в бд
            db.add_user(userInfo[0].id, userLogin, userPassword)
            db.commit()

    #Если пароль и логин введены
    if userLogin != None and userPassword != None:
        #Записать их в бд
        db.edit_account_login(userInfo[0].id, userLogin)
        db.edit_account_password(userInfo[0].id, userPassword)
        db.commit()

    
    #Записываем логин из бд в переменную
    userLogin = db.get_account_login(userInfo[0].id)
    print(userLogin)

    userPassword = db.get_account_password(userInfo[0].id)
    print(userPassword)

    #Авторезируемся в Сетевом Городе
    await ns.login(
        userLogin,
        userPassword,
        'МАОУ "СОШ № 47 г. Челябинска"',
    )

    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {userLogin}')
    #Выходим из СГ
    #await ns.logout()

    #Спустя 10 минут удаляем из памяти дневник ученика
    #await asyncio.sleep(600)
    #diarys.pop(userInfo[0].id)
    #await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')
