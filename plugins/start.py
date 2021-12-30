from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
import ns
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup


bp = Blueprint('start') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр

db = SQLighter('database.db') # Подключаемся к базе данных

ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class StartData(BaseStateGroup):
    city = 10
    school = 11
    clas = 12
    login = 13
    password = 14




@bp.on.message(lev='Начать')
async def city_selection(message: Message):
    await bp.state_dispenser.set(message.peer_id, StartData.city) # Говорим, что следующий шаг - выбор города

    keyboard = (
        Keyboard()
        # Добавить кнопку
        .add(Text('Челябинск'))
        # Новая строка
        .row()
        .add(Text('Волгоград'))
        .row()
        .add(Text('Сан Фиерро'))
        .row()
        .add(Text("Моего города нет в списке", {'cmd': 'not_found'}), color=KeyboardButtonColor.PRIMARY)
    )
    
    await message.answer('Выбери свой город из списка ниже', keyboard=keyboard)



@bp.on.message(state=StartData.city)
async def school_selection(message: Message):
    ctx.set('city', message.text) # Загружаем во временное хранилище город
    await bp.state_dispenser.set(message.peer_id, StartData.clas) # Говорим, что следующий шаг - выбор класса

    keyboard = (
        Keyboard()
        # Добавить кнопку
        .add(Text('МАОУ "СОШ № 47 г. Челябинска"'))
        # Новая строка
        .row()
        .add(Text('ФГКОУ «Волгоградский кадетский корпус...'))
        .row()
        .add(Text('Автошкола SF'))
        .row()
        .add(Text("Моей школы нет в списке", {'cmd': 'not_found'}), color=KeyboardButtonColor.PRIMARY)
    )

    await message.answer('Выбери свою школу', keyboard=keyboard)


@bp.on.message(state=StartData.clas)
async def class_selection(message: Message):
    ctx.set('school', message.text) # Загружаем во внутренне хранилище школу
    await bp.state_dispenser.set(message.peer_id, StartData.school) # Говорим, что следующий шаг - выбор школы

    await message.answer('Окей, теперь напиши в каком ты классе (буква обязательно в нижнем регистре!). \nНапример: 8б.', keyboard=EMPTY_KEYBOARD)


@bp.on.message(state=StartData.school)
async def login_selection(message: Message):
    ctx.set('class', message.text) # Загружаем во внутренне хранилище класс
    await bp.state_dispenser.set(message.peer_id, StartData.login)  # Говорим, что следующий шаг - выбор логина

    await message.answer('Спасибо.\nТеперь введи свой логин', keyboard=EMPTY_KEYBOARD)


@bp.on.message(state=StartData.login)
async def password_selection(message: Message):
    ctx.set('login', message.text) # Загружаем во внутренне хранилище логин
    await bp.state_dispenser.set(message.peer_id, StartData.password)  # Говорим, что следующий шаг - выбор пароля

    await message.answer('Окей, теперь пароль', keyboard=EMPTY_KEYBOARD)
    

@bp.on.private_message(state=StartData.password)
async def end_of_start(message: Message):
    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    city = ctx.get('city') # Берем из временного хранилища город
    school = ctx.get('school') # Берем из временного хранилища школу
    login = ctx.get('login') # Берем из временного хранилища логин
    clas = ctx.get('class') # Берем из временного хранилища класс
    password = message.text 

    # Если город - Челябинск
    if 'Челябинск' in city:
        link = 'https://sgo.edu-74.ru'
    # Если город - Волгоград
    elif 'Волгоград' in city:
        link = 'https://sgo.volganet.ru'

    # Если школа - ...
    if 'ФГКОУ «Волгоградский кадетский корпус...' in school:
        school = 'ФГКОУ «Волгоградский кадетский корпус Следственного комитета Российской Федерации имени Ф.Ф. Слипченко»'
    # Если школа - ...
    elif 'МАОУ "СОШ № 47 г. Челябинска"' in school:
        school = 'МАОУ "СОШ № 47 г. Челябинска"'

    # Если юзер решил шуткануть)
    if 'Сан Фиерро' in city or 'Автошкола SF' in school:
        return 'Давай теперь без рофлов.\nНапиши "Начать"'

    try:
        # Если юзера нет в бд:
        if db.get_account_isFirstLogin(userInfo[0].id) is None:
            db.add_user(userInfo[0].id, login, password, link, school, clas)
            db.commit()
    except TypeError:
        db.add_user(userInfo[0].id, login, password, link, school, clas)
        db.commit()

    else:
        db.edit_account_link(userInfo[0].id, link) # Редактируем бд под новые данные
        db.edit_account_school(userInfo[0].id, school) # Редактируем бд под новые данные
        db.edit_account_login(userInfo[0].id, login) # Редактируем бд под новые данные
        db.edit_account_password(userInfo[0].id, password) # Редактируем бд под новые данные
        db.edit_account_class(userInfo[0].id, clas) # Редактируем бд под новые данные
        db.commit()

    login = db.get_account_login(userInfo[0].id)
    print(login)

    password = db.get_account_password(userInfo[0].id)
    print(password)
    
    school = db.get_account_school(userInfo[0].id)
    print(school)

    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            login,
            password,
            school,
            link
        )
    except:
        await message.answer('Неправильный логин или пароль!')
        return

    db.edit_account_correctData(userInfo[0].id, 1) # Делаем пометку в бд, что у юзера логин и пароль верны
    db.commit()

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}))
    )

    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {login}', keyboard=keyboard)




@bp.on.chat_message(state=StartData.password)
async def end_of_start(message: Message):
    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
    chat_id = message.chat_id
    city = ctx.get('city') # Берем из временного хранилища город
    school = ctx.get('school') # Берем из временного хранилища школу
    login = ctx.get('login') # Берем из временного хранилища логин
    clas = ctx.get('class') # Берем из временного хранилища класс
    password = message.text

    # Если город - Челябинск
    if 'Челябинск' in city:
        link = 'https://sgo.edu-74.ru'
    # Если город - Волгоград
    elif 'Волгоград' in city:
        link = 'https://sgo.volganet.ru'

    # Если школа - ...
    if 'ФГКОУ «Волгоградский кадетский корпус...' in school:
        school = 'ФГКОУ «Волгоградский кадетский корпус Следственного комитета Российской Федерации имени Ф.Ф. Слипченко»'
    # Если школа - ...
    elif 'МАОУ "СОШ № 47 г. Челябинска"' in school:
        school = 'МАОУ "СОШ № 47 г. Челябинска"'


    # Если юзер решил шуткануть)
    if 'Сан Фиерро' in city or 'Автошкола SF' in school:
        return 'Давай теперь без рофлов.\nНапиши "Начать"'

    try:
        # Если чата нет в бд:
        if db.get_chat_login(chat_id) is None:
            db.add_chat(chat_id, login, password, link, school, clas)
            db.commit()
    except TypeError:
        db.add_chat(chat_id, login, password, link, school, clas)
        db.commit()

    else:
        # Редактируем бд под новые данные
        db.edit_chat_link(chat_id, link)
        db.edit_chat_school(chat_id, school)
        db.edit_chat_login(chat_id, login)
        db.edit_chat_password(chat_id, password)
        db.edit_chat_class(chat_id, clas)
        db.commit()

    login = db.get_chat_login(chat_id)
    print(login)

    password = db.get_chat_password(chat_id)
    print(password)

    school = db.get_chat_school(chat_id)
    print(school)

    link = db.get_chat_link(chat_id)
    print(link)

    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            login,
            password,
            school,
            link
        )
    except:
        await message.answer('Неправильный логин или пароль!')
        return

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}))
    )

    await message.answer(f'Эта беседа успешно зашла в систему под логином: {login}', keyboard=keyboard)