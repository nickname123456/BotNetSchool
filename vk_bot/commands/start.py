from database.methods.update import edit_student_clas, edit_student_link, edit_student_login, edit_student_password, edit_student_school, edit_student_studentId, edit_chat_clas, edit_chat_link, edit_chat_login, edit_chat_password, edit_chat_school, edit_chat_studentId, edit_student_vk_id
from database.methods.get import get_all_students, get_chat_by_vk_id, get_student_by_vk_id
from database.methods.create import create_chat, create_student
from database.methods.delete import delete_student
import ns

from vkbottle import BaseStateGroup, CtxStorage, Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import asyncio
import logging


bp = Blueprint('registration')
bp.on.vbml_ignore_case = True # Игнорируем регистр
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
   
class ConnectCodeState(BaseStateGroup):
    INCODE = 19




@bp.on.private_message(text=['начать', '/начать', '/yfxfnm', '/start', '/старт'])
@bp.on.private_message(payload={'cmd': 'start'})
async def registration(message: Message):
    keyboard = Keyboard().add(Text('✔Я уже пользовался "Сетевой Город в ТГ"', {'cmd': f'import_data_from_tg'}))

    await message.answer('Приветствую!👋🏻 Для начала советую ознакомиться с https://vk.com/@botnetschool-spravka-po-ispolzovaniu-bota')
    await message.answer('Продолжая пользоваться этим ботом вы автоматически соглашаетесь с Политикой в отношении обработки персональных данных (https://vk.com/@botnetschool-politika-v-otnoshenii-obrabotki-personalnyh-dannyh)')
    await message.answer('🔗Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/").', keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INLINK)

@bp.on.chat_message(text=['начать', '/начать', '/yfxfnm', '/start', '/старт'])
@bp.on.chat_message(payload={'cmd': 'start'})
async def registration(message: Message):
    await message.answer('Приветствую!👋🏻 Для начала советую ознакомиться с https://vk.com/@botnetschool-spravka-po-ispolzovaniu-bota')
    await message.answer('Продолжая пользоваться этим ботом вы автоматически соглашаетесь с Политикой в отношении обработки персональных данных (https://vk.com/@botnetschool-politika-v-otnoshenii-obrabotki-personalnyh-dannyh)')
    await message.answer('🔗Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/").')
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INLINK)


@bp.on.private_message(payload={'cmd': 'import_data_from_tg'})
async def import_data_from_tg(message: Message):
    await message.answer('🔒Напишите Боту в телеграме "/code" и скопируйте код из сообщения сюда')
    await bp.state_dispenser.set(message.peer_id, ConnectCodeState.INCODE)

@bp.on.private_message(state=ConnectCodeState.INCODE)
async def import_data_from_tg_with_code(message: Message):
    if message.text and len(message.text) == 6 and message.text.isdigit():
        userId = message.from_id
        code = int(message.text)

        for student in get_all_students():
            if student.connect_code == code:
                delete_student(vk_id=userId)
                edit_student_vk_id(telegram_id=student.telegram_id, new_vk_id=userId)

                keyboard = Keyboard().add(Text('Главное меню', {'cmd': 'menu'}), KeyboardButtonColor.POSITIVE)
                await message.answer('✅Вы успешно подключили свой аккаунт ВКонтакте к боту!', keyboard=keyboard)
                await bp.state_dispenser.delete(message.from_id)
                return
    await message.answer('❌Не нашел аккаунта с таким кодом, попробуйте еще раз')


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

    schools = await ns.get_school(ctx.get('link'), ctx.get('countryId'), ctx.get('provincesId'), cityId)
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
    userId = message.from_id # ID юзера
    userInfo =await bp.api.users.get(userId) # Информация о юзере

    link = ctx.get('link')
    countryId = ctx.get('countryId')
    provincesId = ctx.get('provincesId')
    cityId = ctx.get('cityId')
    school = ctx.get('school')
    clas = ctx.get('clas')
    login_without_spaces = ctx.get('login')
    password = message.text

    for i in await ns.get_school(link, countryId, provincesId, cityId):
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

    
    # Если юзера нет в бд:
    if get_student_by_vk_id(userId) is None:
        create_student(vk_id = userId)
        
    edit_student_login(vk_id=userId, new_login=login)
    edit_student_password(vk_id=userId, new_password=password)
    edit_student_link(vk_id=userId, new_link=link)
    edit_student_school(vk_id=userId, new_school=school)
    edit_student_clas(vk_id=userId, new_clas=clas)
    edit_student_studentId(vk_id=userId, new_studentId=studentId)

    logging.info(f'{message.peer_id}: User in database')

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

    for i in await ns.get_school(link, countryId, provincesId, cityId):
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

    
    # Если юзера нет в бд:
    if get_chat_by_vk_id(chat_id) is None:
        create_chat(vk_id=chat_id)

    edit_chat_login(vk_id=chat_id, new_login=login)
    edit_chat_password(vk_id=chat_id, new_password=password)
    edit_chat_link(vk_id=chat_id, new_link=link)
    edit_chat_school(vk_id=chat_id, new_school=school)
    edit_chat_clas(vk_id=chat_id, new_clas=clas)
    edit_chat_studentId(vk_id=chat_id, new_studentId=studentId)

    logging.info(f'{message.peer_id}: User in database')

    keyboard = (
        Keyboard()
        .add(Text('Главное меню', {'cmd': 'menu'}), KeyboardButtonColor.POSITIVE)
    )

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(f'✅Вы успешно зашли в систему под логином: {login}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Start COMPLETED')