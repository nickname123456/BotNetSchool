import asyncio
from vkbottle.bot import Message, Blueprint
from sqlighter import SQLighter
from ns import get_school, get_student
import traceback
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle import BaseStateGroup
import logging
import ns

db = SQLighter('database.db')
bp = Blueprint('registration')




class NewaccountState(BaseStateGroup):
    INLOGIN = 10
    INSCHOOL = 11




@bp.on.message(lev='Начать')
@bp.on.message(payload={'cmd': 'start'})
async def registration(message: Message):
    await message.answer('🖊Введите адрес сетевого города, логин, пароль и класс разделенные пробелом(Пример: "https://sgo.edu-74.ru/ Кирилл~Арз qwerty123 8б").\nЕсли в логине или пароле есть пробелы, то замените их  на ~')
    await bp.state_dispenser.set(message.peer_id, NewaccountState.INLOGIN)



@bp.on.message(state=NewaccountState.INLOGIN)
async def registration2(message: Message):
    logindata = message.text.split(' ')
    if logindata:
        try:
            schools = await get_school(logindata[0])
            await message.answer('📋Введи ID школы из списка ниже(ID - Школа)')
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
            await bp.state_dispenser.set(message.peer_id, NewaccountState.INSCHOOL, logindata=logindata)
        except Exception as e:
            print(traceback.print_exc())
            await message.answer(f'❌Ошибка: {e}\nПопробуйте еще раз или обратитесь к [kirillarz|разработчику]')
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')



@bp.on.private_message(state=NewaccountState.INSCHOOL)
async def registration3(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзерен

    logindata = message.state_peer.payload["logindata"]

    for i in await get_school(logindata[0]):
        if i['id'] == int(message.text):
            school = i['name']
    
    login = ''
    for i in str(logindata[1]):
        if i == '~':
            login+=' '
        else:
            login+=i

    try:
        # Если юзера нет в бд:
        if db.get_account_isFirstLogin(userInfo[0].id) is None:
            db.add_user(userInfo[0].id, login, logindata[2], logindata[0], school, logindata[3])
            db.commit()
        logging.info(f'{message.peer_id}: User in database')
    except TypeError:
        logging.exception(f'{message.peer_id}: User not in database')
        db.add_user(userInfo[0].id, login, logindata[2], logindata[0], school, logindata[3])
        db.commit()

    else:
        db.edit_account_link(userInfo[0].id, logindata[0]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: link')
        db.edit_account_school(userInfo[0].id, school) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: school')
        db.edit_account_login(userInfo[0].id, login) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: login')
        db.edit_account_password(userInfo[0].id, logindata[2]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: password')
        db.edit_account_class(userInfo[0].id, logindata[3]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: clas')
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







@bp.on.chat_message(state=NewaccountState.INSCHOOL)
async def registration3(message: Message):
    chat_id = message.chat_id

    logindata = message.state_peer.payload["logindata"]

    for i in await get_school(logindata[0]):
        if i['id'] == int(message.text):
            school = i['name']

    login = ''
    for i in str(logindata[1]):
        if i == '~':
            login+=' '
        else:
            login+=i

    try:
        # Если юзера нет в бд:
        if db.get_chat_id(chat_id) is None:
            db.add_chat(chat_id, login, logindata[2], logindata[0], school, logindata[3])
            db.commit()
        logging.info(f'{message.peer_id}: User in database')
    except TypeError:
        logging.exception(f'{message.peer_id}: User not in database')
        db.add_chat(chat_id, login, logindata[2], logindata[0], school, logindata[3])
        db.commit()

    else:
        db.edit_chat_link(chat_id, logindata[0]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: link')
        db.edit_chat_school(chat_id, school) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: school')
        db.edit_chat_login(chat_id, login) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: login')
        db.edit_chat_password(chat_id, logindata[2]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: password')
        db.edit_chat_class(chat_id, logindata[3]) # Редактируем бд под новые данные
        logging.info(f'{message.peer_id}: Changed database: clas')
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

