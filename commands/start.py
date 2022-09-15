import asyncio
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from ns import get_school
from vkbottle import BaseStateGroup, CtxStorage, Keyboard, Text, KeyboardButtonColor
import logging
import ns
from VKRules import PayloadStarts

bp = Blueprint('registration')
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



ctx = CtxStorage() # объявляем временное хранилище

class NewaccountState(BaseStateGroup):
    INLINK = 11
    INCOUNTRIES = 12
    INPROVINCES = 13
    INCITIES = 14
    INSCHOOL = 15
    INCLASS = 16
    INLOGIN = 17
    INPASSWORD = 18
   




@bp.on.message(lev='Начать')
@bp.on.message(payload={'cmd': 'start'})
async def registration(message: Message):
    await message.answer('Приветствую!👋🏻 Для начала советую ознакомиться с https://vk.com/@botnetschool-spravka-po-ispolzovaniu-bota')
    await message.answer('Продолжая пользоваться этим ботом вы автоматически соглашаетесь с Политикой в отношении обработки персональных данных (https://vk.com/@botnetschool-politika-v-otnoshenii-obrabotki-personalnyh-dannyh)')
    await message.answer('🔗Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/").')
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INLINK)


@bp.on.message(state=NewaccountState.INLINK)
async def registration_inLink(message: Message):
    if message.attachments:
        if message.attachments[0].link:
            link = 'https://' + str(message.attachments[0].link.caption) + '/'

    if message.text or link:
            if message.text:
                link = message.text

            ctx.set('link', link) # Загружаем во временное хранилище ссылку
            
            try:
                countries = await ns.get_countries(link)
            except:
                await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')
                return
            keyboard = Keyboard()
            for i in countries:
                keyboard.add(Text(i['name'], {'cmd': f'start_countries_{i["id"]}'}))
                keyboard.row()
            keyboard.add(Text('Назад', {'cmd': 'start'}), color = KeyboardButtonColor.NEGATIVE)

            await message.answer('🌍В какой стране вы живете?', keyboard=keyboard)
            await bp.state_dispenser.set(message.peer_id, NewaccountState.INCOUNTRIES)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')

@bp.on.message(state=NewaccountState.INCOUNTRIES, PayloadStarts='{"cmd":"start_countries_')
async def registration_inCountries(message: Message):
    countryId = int(message.payload[24:-2])

    ctx.set('countryId', countryId) # Загружаем во временное хранилище ссылку
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INPROVINCES)

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'start'}), color = KeyboardButtonColor.NEGATIVE)
    )

    provinces = await ns.get_provinces(ctx.get('link'), countryId)
    text = ''
    for i in provinces:
        text += f'\n"{i["id"]}" - {i["name"]}'

    await message.answer('📋Введите ID района/области из списка ниже', keyboard=keyboard)

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(text[x:x+4096])
            await asyncio.sleep(1,5)
        await message.answer('✅Всё!')
    else:
        await message.answer(text)

@bp.on.message(state=NewaccountState.INPROVINCES)
async def registration_inProvinces(message: Message):
    try:
        provincesId = int(message.text)
    except:
        await message.answer('❌Не нашел в твоем сообщении данные, введите еще раз')
        return

    ctx.set('provincesId', provincesId) # Загружаем во временное хранилище ссылку
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INCITIES)

    keyboard = Keyboard().add(Text('Назад', {'cmd': 'start'}), color = KeyboardButtonColor.NEGATIVE)

    cities = await ns.get_cities(ctx.get('link'), ctx.get('countryId'), provincesId)
    text = ''
    for i in cities:
        text += f"\n{i['id']} - {i['name']}"

    await message.answer('📋Введите ID города из списка ниже', keyboard=keyboard)

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(text[x:x+4096])
            await asyncio.sleep(1,5)
        await message.answer('✅Всё!')
    else:
        await message.answer(text)

@bp.on.message(state=NewaccountState.INCITIES)
async def registration_inCities(message: Message):
    try:
        cityId = int(message.text)
    except:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')

    ctx.set('cityId', cityId) # Загружаем во временное хранилище ссылку
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INSCHOOL)

    keyboard = Keyboard().add(Text('Назад', {'cmd': 'start'}), color = KeyboardButtonColor.NEGATIVE)

    schools = await get_school(ctx.get('link'), ctx.get('countryId'), ctx.get('provincesId'), cityId)
    text = ''
    for i in schools:
        text += f"\n{i['id']} - {i['name']}"

    await message.answer('📋Введите ID школы из списка ниже', keyboard=keyboard)

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(text[x:x+4096])
            await asyncio.sleep(1,5)
        await message.answer('✅Всё!')
    else:
        await message.answer(text)
   



@bp.on.message(state=NewaccountState.INSCHOOL)
async def registration_inSchool(message: Message):
    if message.text.isdigit():
        ctx.set('school', message.text) # Загружаем во временное хранилище школу

        await message.answer('🖊Введите свой класс (Пример: "8б").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INCLASS)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')


@bp.on.message(state=NewaccountState.INCLASS)
async def registration_inClass(message: Message):
    if message.text:
        ctx.set('clas', message.text.lower()) # Загружаем во временное хранилище класс

        await message.answer('🖊Введите свой логин из СГО (Пример: "nickname123456").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INLOGIN)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')


@bp.on.message(state=NewaccountState.INLOGIN)
async def registration_inLogin(message: Message):
    if message.text:
        ctx.set('login', message.text) # Загружаем во временное хранилище логин

        await message.answer('🔑Введите свой пароль из СГО (Пример: "qwerty1234").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INPASSWORD)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')



@bp.on.private_message(state=NewaccountState.INPASSWORD)
async def private_registration_inPassword(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере

    link = ctx.get('link')
    countryId = ctx.get('countryId')
    provincesId = ctx.get('provincesId')
    cityId = ctx.get('cityId')
    school = ctx.get('school')
    clas = ctx.get('clas')
    login_without_spaces = ctx.get('login')
    password = message.text

    for i in await get_school(link, countryId, provincesId, cityId):
        if i['id'] == int(school):
            school = i['name']
            break
    
    login = ""
    for i in str(login_without_spaces):
        if i == '~':
            login+=' '
        else:
            login+=i

    try:
        studentId = await ns.getCurrentStudentId(login, password, school, link)
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин, пароль или школа!\n 🤔Попробуйте еще раз')
        await registration(message) # Отправляем обратно вводить все данные
        return

    try:
        # Если юзера нет в бд:
        if db.get_account_isFirstLogin(userInfo[0].id) is None:
            db.add_user(userInfo[0].id, login, password, link, school, clas, studentId)
            db.commit()
        logging.info(f'{message.peer_id}: User in database')
    except TypeError:
        logging.exception(f'{message.peer_id}: User not in database')
        db.add_user(userInfo[0].id, login, password, link, school, clas, studentId)
        db.commit()

    else:
        db.edit_account_link(userInfo[0].id, link) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: link')
        db.edit_account_school(userInfo[0].id, school) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: school')
        db.edit_account_login(userInfo[0].id, login) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: login')
        db.edit_account_password(userInfo[0].id, password) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: password')
        db.edit_account_class(userInfo[0].id, clas) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: clas')
        db.edit_account_studentId(userInfo[0].id, studentId) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: studentId')
        db.commit()

    db.edit_account_correctData(userInfo[0].id, 1) # Делаем пометку в бд, что у юзера логин и пароль верны
    db.commit()
    logging.info(f'{message.peer_id}: We make a note in the database that the user login and password are correct')

    keyboard = (
        Keyboard()
        .add(Text('Главное меню', {'cmd': 'menu'}), KeyboardButtonColor.POSITIVE)
    )

    await bp.state_dispenser.delete(message.from_id)
    await message.answer(f'✅{userInfo[0].first_name}, вы успешно зашли в систему под логином: {login}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Start COMPLETED')







@bp.on.chat_message(state=NewaccountState.INPASSWORD)
async def chat_registration_inPassword(message: Message):
    chat_id = message.chat_id

    link = ctx.get('link')
    countryId = ctx.get('countryId')
    provincesId = ctx.get('provincesId')
    cityId = ctx.get('cityId')
    school = ctx.get('school')
    clas = ctx.get('clas')
    login_without_spaces = ctx.get('login')
    password = message.text

    for i in await get_school(link, countryId, provincesId, cityId):
        if i['id'] == int(school):
            school = i['name']
            break

    login = ''
    for i in str(login_without_spaces):
        if i == '~':
            login+=' '
        else:
            login+=i
            
    try:
        studentId = await ns.getCurrentStudentId(login, password, school, link)
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин, пароль или школа!\n 🤔Попробуйте еще раз')
        await registration(message) # Отправляем обратно вводить все данные
        return

    try:
        # Если юзера нет в бд:
        if db.get_chat_id(chat_id) is None:
            db.add_chat(chat_id, login, password, link, school, clas, studentId)
            db.commit()
        logging.info(f'{message.peer_id}: User in database')
    except TypeError:
        logging.exception(f'{message.peer_id}: User not in database')
        db.add_chat(chat_id, login, password, link, school, clas, studentId)
        db.commit()

    else:
        db.edit_chat_link(chat_id, link) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: link')
        db.edit_chat_school(chat_id, school) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: school')
        db.edit_chat_login(chat_id, login) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: login')
        db.edit_chat_password(chat_id, password) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: password')
        db.edit_chat_class(chat_id, clas) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: clas')
        db.edit_chat_studentId(chat_id, studentId) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: studentId')
        db.commit()

    keyboard = (
        Keyboard()
        .add(Text('Главное меню', {'cmd': 'menu'}), KeyboardButtonColor.POSITIVE)
    )

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(f'✅Вы успешно зашли в систему под логином: {login}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Start COMPLETED')