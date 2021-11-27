from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
import ns
import netschoolapi
from vkbottle import CtxStorage
from vkbottle_types import BaseStateGroup


bp = Blueprint('start')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')

ctx = CtxStorage()


class StartData(BaseStateGroup):
    city = 10
    school = 11
    login = 12
    password = 13


@bp.on.chat_message(text='Начать')
async def start(message: Message):
    await message.answer('Доступно только в ЛС!')



@bp.on.private_message(lev='Начать')
async def city_selection(message: Message):
    await bp.state_dispenser.set(message.peer_id, StartData.city)

    keyboard = (
        Keyboard()
        .add(Text('Челябинск'))
        .row()
        .add(Text('Волгоград'))
        .row()
        .add(Text('Сан Фиерро'))
        .row()
        .add(Text("Моего города нет в списке", {'cmd': 'not_found'}), color=KeyboardButtonColor.PRIMARY)
    )
    
    await message.answer('Выбери свой город из списка ниже', keyboard=keyboard)



@bp.on.private_message(state=StartData.city)
async def school_selection(message: Message):
    ctx.set('city', message.text)
    await bp.state_dispenser.set(message.peer_id, StartData.school)

    keyboard = (
        Keyboard()
        .add(Text('МАОУ "СОШ № 47 г. Челябинска"'))
        .row()
        .add(Text('ФГКОУ «Волгоградский кадетский корпус...'))
        .row()
        .add(Text('Автошкола SF'))
        .row()
        .add(Text("Моей школы нет в списке", {'cmd': 'not_found'}), color=KeyboardButtonColor.PRIMARY)
    )

    await message.answer('Выбери свою школу', keyboard=keyboard)


@bp.on.private_message(state=StartData.school)
async def login_selection(message: Message):
    ctx.set('school', message.text)
    await bp.state_dispenser.set(message.peer_id, StartData.login)

    await message.answer('Спасибо.\nТеперь введи свой логин', keyboard=EMPTY_KEYBOARD)


@bp.on.private_message(state=StartData.login)
async def password_selection(message: Message):
    ctx.set('login', message.text)
    await bp.state_dispenser.set(message.peer_id, StartData.password)

    await message.answer('Окей, теперь пароль', keyboard=EMPTY_KEYBOARD)
    

@bp.on.private_message(state=StartData.password)
async def end_of_start(message: Message):
    await bp.state_dispenser.delete(message.peer_id)
    userInfo = await bp.api.users.get(message.from_id)
    city = ctx.get('city')
    school = ctx.get('school')
    login = ctx.get('login')
    password = message.text

    if 'Челябинск' in city:
        link = 'https://sgo.edu-74.ru'
    elif 'Волгоград' in city:
        link = 'https://sgo.volganet.ru'

    if 'ФГКОУ «Волгоградский кадетский корпус...' in school:
        school = 'ФГКОУ «Волгоградский кадетский корпус Следственного комитета Российской Федерации имени Ф.Ф. Слипченко»'
    elif 'МАОУ "СОШ № 47 г. Челябинска"' in school:
        school = 'МАОУ "СОШ № 47 г. Челябинска"'


    if 'Сан Фиерро' in city or 'Автошкола SF' in school:
        return 'Давай теперь без рофлов.\nНапиши "Начать"'

    if db.get_account_isFirstLogin(userInfo[0].id) is None:
        db.add_user(userInfo[0].id, login, password, link, school)
        db.commit()

    else:
        db.edit_account_link(userInfo[0].id, link)
        db.edit_account_school(userInfo[0].id, school)
        db.edit_account_login(userInfo[0].id, login)
        db.edit_account_password(userInfo[0].id, password)
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

    db.edit_account_correctData(userInfo[0].id, 1)
    db.commit()

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}))
    )

    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {login}', keyboard=keyboard)
