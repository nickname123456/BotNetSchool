import asyncio
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from ns import get_school
import traceback
from vkbottle import Keyboard,  Text
from vkbottle import BaseStateGroup
import logging
import ns
from vkbottle import CtxStorage

bp = Blueprint('registration')



ctx = CtxStorage() # объявляем временное хранилище

class NewaccountState(BaseStateGroup):
    INLINK = 11
    INSCHOOL = 12
    INCLASS = 13
    INLOGIN = 14
    INPASSWORD = 15
   




@bp.on.message(lev='Начать')
@bp.on.message(payload={'cmd': 'start'})
async def registration(message: Message):
    await message.answer('🖊Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/").')
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INLINK)



@bp.on.message(state=NewaccountState.INLINK)
async def registration2(message: Message):
    if message.attachments:
        if message.attachments[0].link:
            link = 'https://' + str(message.attachments[0].link.caption) + '/'

    if message.text or link:
        try:
            if message.text:
                link = message.text

            ctx.set('link', link) # Загружаем во временное хранилище ссылку

            schools = await get_school(link)
            await message.answer('📋Введи ID школы из списка ниже(ID - Школа)')
            await asyncio.sleep(2)
            text = ''
            for school in schools:
                text += f"\n{school['id']} - {school['name']}"
            if len(text) > 4096:
                for x in range(0, len(text), 4096):
                    await message.answer(text[x:x+4096])
                    await asyncio.sleep(1,5)
                await message.answer('✅Всё!')
            else:
                await message.answer(text)
            await bp.state_dispenser.set(message.peer_id, NewaccountState.INSCHOOL)
        except Exception as e:
            print(traceback.print_exc())
            await message.answer(f'❌Ошибка: {e}\nПопробуйте еще раз или обратитесь к [kirillarz|разработчику]')
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')



@bp.on.message(state=NewaccountState.INSCHOOL)
async def registration3(message: Message):
    if message.text:
        ctx.set('school', message.text) # Загружаем во временное хранилище школу

        await message.answer('🖊Введите свой класс (Пример: "8б").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INCLASS)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')


@bp.on.message(state=NewaccountState.INCLASS)
async def registration4(message: Message):
    if message.text:
        ctx.set('clas', message.text) # Загружаем во временное хранилище класс

        await message.answer('🖊Введите свой логин из СГО (Пример: "nickname123456").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INLOGIN)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')


@bp.on.message(state=NewaccountState.INLOGIN)
async def registration5(message: Message):
    if message.text:
        ctx.set('login', message.text) # Загружаем во временное хранилище логин

        await message.answer('🖊Введите свой пароль из СГО (Пример: "qwerty1234").')
        await bp.state_dispenser.set(message.peer_id, NewaccountState.INPASSWORD)
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')



@bp.on.private_message(state=NewaccountState.INPASSWORD)
async def private_registration6(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере

    link = ctx.get('link')
    school = ctx.get('school')
    clas = ctx.get('clas')
    login_without_spaces = ctx.get('login')
    password = message.text

    for i in await get_school(link):
        if i['id'] == int(school):
            school = i['name']
            break
    
    login = ""
    for i in str(login_without_spaces):
        if i == '~':
            login+=' '
        else:
            login+=i

    studentId = await ns.getCurrentStudentId(login, password, school, link)
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


    
    login = db.get_account_login(userInfo[0].id)
    password = db.get_account_password(userInfo[0].id)
    school = db.get_account_school(userInfo[0].id)
    link = db.get_account_link(userInfo[0].id)
    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            login,
            password,
            school,
            link
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!')
        return

    db.edit_account_correctData(userInfo[0].id, 1) # Делаем пометку в бд, что у юзера логин и пароль верны
    db.commit()
    logging.info(f'{message.peer_id}: We make a note in the database that the user login and password are correct')

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}))
    )

    
    await bp.state_dispenser.delete(message.from_id)
    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {login}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Start COMPLETED')







@bp.on.chat_message(state=NewaccountState.INPASSWORD)
async def chat_registration6(message: Message):
    chat_id = message.chat_id

    link = ctx.get('link')
    school = ctx.get('school')
    clas = ctx.get('clas')
    login_without_spaces = ctx.get('login')
    password = message.text

    for i in await get_school(link):
        if i['id'] == int(school):
            school = i['name']
            break

    login = ''
    for i in str(login_without_spaces):
        if i == '~':
            login+=' '
        else:
            login+=i
            
    studentId = await ns.getCurrentStudentId(login, password, school, link)
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


    
    login = db.get_chat_login(chat_id)
    password = db.get_chat_password(chat_id)
    school = db.get_chat_school(chat_id)
    link = db.get_chat_link(chat_id)
    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            login,
            password,
            school,
            link
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!')
        return

    logging.info(f'{message.peer_id}: We make a note in the database that the user login and password are correct')

    keyboard = (
        Keyboard()
        .add(Text('Назад', {'cmd': 'menu'}))
    )

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(f'Ты успешно зашел в систему под логином: {login}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: Start COMPLETED')

