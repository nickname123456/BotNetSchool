from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from netschoolapi import NetSchoolAPI
import netschoolapi
from sqlighter import SQLighter
import ns


bp = Blueprint('login')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')



#Если написали "Вход" или нажали на соответствующую кнопку
@bp.on.private_message(text=["Вход <userLogin> <userPassword>", "Вход"])
@bp.on.private_message(payload={'cmd': 'login'})
async def login(message: Message, userLogin=None, userPassword=None):
    #Собираем инфу о пользователе
    userInfo = await bp.api.users.get(message.from_id)

    
    if db.get_account_isFirstLogin(userInfo[0].id) is None:
        await message.answer("Так... Смотрю тебя теще нет в моей бд. Но ничего страшного сейчас все будет!")
        await message.answer('Напиши "Начать')
        return

    #Если пароль и логин введены
    if userLogin != None and userPassword != None:
        #Записать их в бд
        db.edit_account_login(userInfo[0].id, userLogin)
        db.edit_account_password(userInfo[0].id, userPassword)
        db.edit_account_correctData(userInfo[0].id, 0)
        db.commit()

    
    #Записываем логин из бд в переменную
    userLogin = db.get_account_login(userInfo[0].id)
    print(userLogin)

    userPassword = db.get_account_password(userInfo[0].id)
    print(userPassword)

    userSchool = db.get_account_school(userInfo[0].id)
    print(userSchool)

    userLink = db.get_account_link(userInfo[0].id)
    print(userLink)

    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            userLogin,
            userPassword,
            userSchool,
            userLink
        )
    except:
        await message.answer('Неправильный логин или пароль!')
        return

    db.edit_account_correctData(userInfo[0].id, 1)
    db.commit()

    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {userLogin}')
    #Выходим из СГ
    #await ns.logout()

    #Спустя 10 минут удаляем из памяти дневник ученика
    #await asyncio.sleep(600)
    #diarys.pop(userInfo[0].id)
    #await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')




@bp.on.chat_message(text=["Вход <userLogin> <userPassword>", "Вход"])
@bp.on.chat_message(payload={'cmd': 'login'})
async def login(message: Message, userLogin=None, userPassword=None):
    chat_id = message.chat_id

    try:

        #Если пароль и логин введены
        if userLogin != None and userPassword != None:
            #Записать их в бд
            db.edit_chat_login(chat_id, userLogin)
            db.edit_chat_password(chat_id, userPassword)
            db.commit()

        
        #Записываем логин из бд в переменную
        chatLogin = db.get_chat_login(chat_id)
        print(chatLogin)

        chatPassword = db.get_chat_password(chat_id)
        print(chatPassword)

        chatSchool = db.get_chat_school(chat_id)
        print(chatSchool)

        chatLink = db.get_chat_link(chat_id)
        print(chatLink)

        #Авторезируемся в Сетевом Городе
        await ns.login(
            chatLogin,
            chatPassword,
            chatSchool,
            chatLink)
            
    except TypeError:
        await message.answer('Нужно зарегистрировать беседу. \nНапиши "Начать"')
        return

    except:
        await message.answer('Неправильный логин или пароль!')
        return

    await message.answer(f'Эта беседа успешно зашла в систему под логином: {chatLogin}')
    #Выходим из СГ
    #await ns.logout()

    #Спустя 10 минут удаляем из памяти дневник ученика
    #await asyncio.sleep(600)
    #diarys.pop(userInfo[0].id)
    #await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')
