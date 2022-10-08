from database.methods.delete import delete_chat
from database.methods.update import edit_chat_clas, edit_chat_link, edit_chat_login, edit_chat_password, edit_chat_school, edit_chat_studentId, edit_chat_telegram_id
from database.methods.get import get_all_chats, get_all_students, get_chat_by_telegram_id
from database.methods.create import create_chat

from tg_bot.states import StartStates, ConnectCodeStates
import ns

from aiogram.types import Message, InlineKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher

import logging



async def registration(message: Message):
    bot = message.bot
    chat_id = message.chat.id
    kb = InlineKeyboardMarkup().add(KeyboardButton('✔Импортировать настройки из Личных Сообщений', callback_data='import_data_from_private'))

    await bot.send_message(chat_id, 'Приветствую!👋🏻 Для начала советую ознакомиться с https://vk.com/@botnetschool-spravka-po-ispolzovaniu-bota')
    await bot.send_message(chat_id, 'Продолжая пользоваться этим ботом вы автоматически соглашаетесь с Политикой в отношении обработки персональных данных (https://vk.com/@botnetschool-politika-v-otnoshenii-obrabotki-personalnyh-dannyh)')
    await bot.send_message(chat_id, '🔗Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/"). \nЕсли вы уже пользовались "Сетевой Город в ВК", то нажмите на кнопку ниже.', reply_markup=kb)

    await StartStates.INLINK.set()


async def registration_inLink(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.chat.id
    link = message.text

    try:
        countries = await ns.get_countries(link)
    except:
        await bot.send_message(chat_id, '❌Не нашел в твоем сообщении данные, введи еще раз')
        return

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in countries:
        keyboard.add(KeyboardButton(i['name'], callback_data=f'start_countries_{i["id"]}'))
    keyboard.add(KeyboardButton('🔙Назад', callback_data=f'start_back'))
    
    await state.update_data(link=link)
    await StartStates.next()
    await bot.send_message(chat_id, '🌍В какой стране вы живете?', reply_markup=keyboard)
    
    

async def registration_inCountries(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message

    countryId = callback_query.data[16:]

    await state.update_data(countryId=countryId)
    await StartStates.next()

    provinces = await ns.get_provinces((await state.get_data())['link'], countryId)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in provinces:
        keyboard.insert(KeyboardButton(i['name'], callback_data=f'start_provinces_{i["id"]}'))
    keyboard.add(KeyboardButton('🔙Назад', callback_data=f'start_back'))

    await message.edit_text('📋Введите ID района/области из списка ниже')
    await message.edit_reply_markup(keyboard)



async def registration_inProvinces(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message

    link = (await state.get_data())['link']
    countryId = (await state.get_data())['countryId']
    provincesId = callback_query.data[16:]

    await state.update_data(provincesId=provincesId)
    await StartStates.next()

    provinces = await ns.get_cities(link, countryId, provincesId)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in provinces:
        keyboard.insert(KeyboardButton(i['name'], callback_data=f'start_cities_{i["id"]}'))
    keyboard.add(KeyboardButton('🔙Назад', callback_data=f'start_back'))

    await message.edit_text('📋В каком городе вы живете?')
    await message.edit_reply_markup(keyboard)



async def registration_inCities(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    bot = message.bot
    chat_id = message.chat.id

    link = (await state.get_data())['link']
    countryId = (await state.get_data())['countryId']
    provincesId = (await state.get_data())['provincesId']
    cityId = callback_query.data[13:]

    await state.update_data(cityId=cityId)
    await StartStates.next()

    schools = await ns.get_school(link, countryId, provincesId, cityId)
    text = ''
    for i in schools:
        text += f"\n{i['id']} - {i['name']}"

    kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))
    await message.edit_text('📋Введите ID школы из списка ниже')

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(chat_id, text[x:x+4096])
        await bot.send_message(chat_id, '✅Всё!', reply_markup=kb)
    else:
        await bot.send_message(chat_id, text, reply_markup=kb)

async def registration_inSchools(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.chat.id
    if message.text.isdigit():
        await state.update_data(school=message.text) # Загружаем во временное хранилище школу

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(chat_id, '🖊Введите свой класс (Пример: "8б").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(chat_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)


async def registration_inClass(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.chat.id
    if message.text:
        await state.update_data(clas=message.text.lower()) # Загружаем во временное хранилище класс

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(chat_id, '🖊Введите свой логин из СГО (Пример: "nickname123456").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(chat_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)

async def registration_inLogin(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.chat.id
    if message.text:
        await state.update_data(login=message.text) # Загружаем во временное хранилище логин

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(chat_id, '🔑Введите свой пароль из СГО (Пример: "qwerty1234").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(chat_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)
    
async def registration_inPassword(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.chat.id
    kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))
    if message.text is None:
        return await bot.send_message(chat_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)

    all_data = await state.get_data()
    link = all_data['link']
    countryId = all_data['countryId']
    provincesId = all_data['provincesId']
    cityId = all_data['cityId']
    school = all_data['school']
    clas = all_data['clas']
    login = all_data['login']
    password = message.text

    for i in await ns.get_school(link, countryId, provincesId, cityId):
        if i['id'] == int(school):
            school = i['name']
            break
    
    try:
        studentId = await ns.getCurrentStudentId(login, password, school, link)
        logging.info(f'{chat_id}: Login in NetSchool')
    except:
        logging.exception(f'{chat_id}: Exception occurred')
        await bot.send_message(chat_id, '❌Неправильный логин, пароль или школа!\n 🤔Попробуйте еще раз', reply_markup=kb)
        await registration(message) # Отправляем обратно вводить все данные
        return

    # Если юзера нет в бд:
    if get_chat_by_telegram_id(chat_id) is None:
        create_chat(telegram_id= chat_id)
        
    edit_chat_login(telegram_id=chat_id, new_login=login)
    edit_chat_password(telegram_id=chat_id, new_password=password)
    edit_chat_link(telegram_id=chat_id, new_link=link)
    edit_chat_school(telegram_id=chat_id, new_school=school)
    edit_chat_clas(telegram_id=chat_id, new_clas=clas)
    edit_chat_studentId(telegram_id=chat_id, new_studentId=studentId)
    logging.info(f'{chat_id}: User in database')

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🏠Главное меню', callback_data='main_menu'))

    await bot.send_message(chat_id, '✅Вы успешно зарегистрировались!', reply_markup=keyboard)
    await state.finish()
    logging.info(f'{chat_id}: Start COMPLETED')



async def import_data_from_private(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    await ConnectCodeStates.INCODE.set()
    await message.answer('🔒Напишите мне в Личные Сообщения "/code" и введите код, который я вам отправлю в ответ.\n\n🔑После этого я смогу получить данные из вашего аккаунта.')

async def import_data_from_private_with_code(message: Message, state: FSMContext):
    if message.text and len(message.text) == 6 and message.text.isdigit():
        chat_id = message.chat.id
        code = int(message.text)

        for student in get_all_students():
            if student.connect_code == code:
                if get_chat_by_telegram_id(chat_id) is None:
                    create_chat(telegram_id= chat_id)
                edit_chat_login(telegram_id=chat_id, new_login=student.login)
                edit_chat_password(telegram_id=chat_id, new_password=student.password)
                edit_chat_link(telegram_id=chat_id, new_link=student.link)
                edit_chat_school(telegram_id=chat_id, new_school=student.school)
                edit_chat_clas(telegram_id=chat_id, new_clas=student.clas)
                edit_chat_studentId(telegram_id=chat_id, new_studentId=student.studentId)
                logging.info(f'{chat_id}: Chat in database')

                keyboard = InlineKeyboardMarkup(resize_keyboard=True)
                keyboard.add(KeyboardButton('🏠Главное меню', callback_data='main_menu'))

                await message.answer('✅Вы успешно зарегистрировались!', reply_markup=keyboard)
                await state.finish()
                return
    await message.answer('❌Не нашел аккаунта с таким кодом, попробуйте еще раз')



async def start_back(message: Message , callback_query: CallbackQuery = None):
    bot = message.bot
    chat_id = message.chat.id
    if callback_query is not None:
        message = callback_query.message
    await bot.send_message(chat_id, '🔙Возвращаемся назад...')
    await registration(message)


def register_chat_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_back, content_types=['text'], text=['назад', 'Назад', '🔙Назад'], state='*', chat_type='group')

    dp.register_callback_query_handler(import_data_from_private, lambda c: c.data and c.data.startswith('import_data_from_private'), state='*', chat_type='group')
    dp.register_message_handler(import_data_from_private_with_code, state=ConnectCodeStates.INCODE, chat_type='group')

    dp.register_callback_query_handler(start_back, lambda c: c.data and c.data == 'start_back', state='*', chat_type='group')
    dp.register_message_handler(registration, content_types=['text'], text=['начать', '/начать', '/yfxfnm', '/start', '/старт'], chat_type='group')
    dp.register_message_handler(registration_inLink, state=StartStates.INLINK, chat_type='group')
    dp.register_callback_query_handler(registration_inCountries, lambda c: c.data and c.data.startswith('start_countries_'), state=StartStates.INCOUNTRIES, chat_type='group')
    dp.register_callback_query_handler(registration_inProvinces, lambda c: c.data and c.data.startswith('start_provinces_'), state=StartStates.INPROVINCES, chat_type='group')
    dp.register_callback_query_handler(registration_inCities, lambda c: c.data and c.data.startswith('start_cities_'), state=StartStates.INCITIES, chat_type='group')
    dp.register_message_handler(registration_inSchools, state=StartStates.INSCHOOL, chat_type='group')
    dp.register_message_handler(registration_inClass, state=StartStates.INCLASS, chat_type='group')
    dp.register_message_handler(registration_inLogin, state=StartStates.INLOGIN, chat_type='group')
    dp.register_message_handler(registration_inPassword, state=StartStates.INPASSWORD, chat_type='group')



