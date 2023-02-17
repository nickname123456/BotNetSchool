from database.methods.delete import delete_student
from database.methods.update import edit_student_clas, edit_student_link, edit_student_login, edit_student_password, edit_student_school, edit_student_studentId, edit_student_telegram_id
from database.methods.get import get_all_students, get_student_by_telegram_id
from database.methods.create import create_student

from tg_bot.keyboards.inline import kb_back_to_start_from_code
from tg_bot.states import StartStates, ConnectCodeStates
import ns

from aiogram.types import Message, InlineKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher

from urllib.parse import urlparse
import logging



async def registration(message: Message):
    bot = message.bot
    user_id = message.from_user.id
    kb = InlineKeyboardMarkup().add(KeyboardButton('✔Я уже пользовался "Сетевой Город в ВК"', callback_data='import_data_from_vk'))

    await bot.send_message(user_id, 'Приветствую!👋🏻 Для начала советую ознакомиться с https://vk.com/@botnetschool-spravka-po-ispolzovaniu-bota')
    await bot.send_message(user_id, 'Продолжая пользоваться этим ботом вы автоматически соглашаетесь с Политикой в отношении обработки персональных данных (https://vk.com/@botnetschool-politika-v-otnoshenii-obrabotki-personalnyh-dannyh)')
    await bot.send_message(user_id, '🔗Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/"). \nЕсли вы уже пользовались "Сетевой Город в ВК", то нажмите на кнопку ниже.', reply_markup=kb)

    await StartStates.INLINK.set()


async def registration_inLink(message: Message, state: FSMContext):
    bot = message.bot
    user_id = message.from_user.id
    link = urlparse(message.text)
    link = f'{link.scheme}://{link.netloc}'

    try:
        countries = await ns.get_countries(link)
    except:
        await bot.send_message(user_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb_back_to_start_from_code)
        return

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in countries:
        keyboard.add(KeyboardButton(i['name'], callback_data=f'start_countries_{i["id"]}'))
    keyboard.add(KeyboardButton('🔙Назад', callback_data=f'start_back'))
    
    await state.update_data(link=link)
    await StartStates.next()
    await bot.send_message(user_id, '🌍В какой стране вы живете?', reply_markup=keyboard)
    
    

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
    user_id = callback_query.from_user.id

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
            await bot.send_message(user_id, text[x:x+4096])
        await bot.send_message(user_id, '✅Всё!', reply_markup=kb)
    else:
        await bot.send_message(user_id, text, reply_markup=kb)

async def registration_inSchools(message: Message, state: FSMContext):
    bot = message.bot
    user_id = message.from_user.id
    if message.text.isdigit():
        await state.update_data(school=message.text) # Загружаем во временное хранилище школу

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(user_id, '🖊Введите свой класс (Пример: "8б").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(user_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)


async def registration_inClass(message: Message, state: FSMContext):
    bot = message.bot
    user_id = message.from_user.id
    if message.text:
        await state.update_data(clas=message.text.lower()) # Загружаем во временное хранилище класс

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(user_id, '🖊Введите свой логин из СГО (Пример: "nickname123456").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(user_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)

async def registration_inLogin(message: Message, state: FSMContext):
    bot = message.bot
    user_id = message.from_user.id
    if message.text:
        await state.update_data(login=message.text) # Загружаем во временное хранилище логин

        kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))

        await bot.send_message(user_id, '🔑Введите свой пароль из СГО (Пример: "qwerty1234").', reply_markup=kb)
        await StartStates.next()
    else:
        await bot.send_message(user_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)
    
async def registration_inPassword(message: Message, state: FSMContext):
    bot = message.bot
    user_id = message.from_user.id
    kb = InlineKeyboardMarkup().add(KeyboardButton('🔙Назад', callback_data='start_back'))
    if message.text is None:
        return await bot.send_message(user_id, '❌Не нашел в твоем сообщении данные, введи еще раз', reply_markup=kb)
    
    userId = message.from_user.id

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
        logging.info(f'{userId}: Login in NetSchool')
    except:
        logging.exception(f'{userId}: Exception occurred')
        await bot.send_message(user_id, '❌Неправильный логин, пароль или школа!\n 🤔Попробуйте еще раз', reply_markup=kb)
        await registration(message) # Отправляем обратно вводить все данные
        return

    # Если юзера нет в бд:
    if get_student_by_telegram_id(userId) is None:
        create_student(telegram_id= userId)
        
    edit_student_login(telegram_id=userId, new_login=login)
    edit_student_password(telegram_id=userId, new_password=password)
    edit_student_link(telegram_id=userId, new_link=link)
    edit_student_school(telegram_id=userId, new_school=school)
    edit_student_clas(telegram_id=userId, new_clas=clas)
    edit_student_studentId(telegram_id=userId, new_studentId=studentId)
    logging.info(f'{userId}: User in database')

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🏠Главное меню', callback_data='main_menu'))

    await bot.send_message(user_id, '✅Вы успешно зарегистрировались!', reply_markup=keyboard)
    await state.finish()
    logging.info(f'{userId}: Start COMPLETED')



async def import_data_from_vk(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    await ConnectCodeStates.INCODE.set()
    await message.answer('🔒Напишите в ЛС Боту ВКонтакте "/code" и скопируйте код из сообщения сюда')

async def import_data_from_vk_with_code(message: Message, state: FSMContext):
    if message.text and len(message.text) == 6 and message.text.isdigit():
        userId = message.from_user.id
        code = int(message.text)

        for student in get_all_students():
            if student.connect_code == code:
                delete_student(telegram_id=userId)
                edit_student_telegram_id(vk_id=student.vk_id, new_telegram_id=userId)

                keyboard = InlineKeyboardMarkup(resize_keyboard=True)
                keyboard.add(KeyboardButton('🏠Главное меню', callback_data='main_menu'))

                await message.answer('✅Вы успешно подключили свой аккаунт ВКонтакте к боту!', reply_markup=keyboard)
                await state.finish()
                return
    await message.answer('❌Не нашел аккаунта с таким кодом, попробуйте еще раз', reply_markup=kb_back_to_start_from_code)



async def start_back(message: Message = None, callback_query: CallbackQuery = None):
    bot = message.bot
    if isinstance(message, CallbackQuery):
        message = message.message
    user_id = message.from_user.id
    await bot.send_message(user_id, '🔙Возвращаемся назад...')
    await registration(message)


def register_user_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_back, content_types=['text'], text=['назад', 'Назад', '🔙Назад'], state='*', chat_type='private')
    dp.register_message_handler(start_back, commands=['start_back'], state='*', chat_type='private')

    dp.register_callback_query_handler(import_data_from_vk, lambda c: c.data and c.data.startswith('import_data_from_vk'), state='*', chat_type='private')
    dp.register_message_handler(import_data_from_vk_with_code, state=ConnectCodeStates.INCODE, chat_type='private')

    dp.register_callback_query_handler(start_back, lambda c: c.data and c.data == 'start_back', state='*', chat_type='private')
    dp.register_message_handler(registration, content_types=['text'], text=['начать', '/начать', '/yfxfnm', '/start', '/старт'], chat_type='private')
    dp.register_message_handler(registration_inLink, state=StartStates.INLINK, chat_type='private')
    dp.register_callback_query_handler(registration_inCountries, lambda c: c.data and c.data.startswith('start_countries_'), state=StartStates.INCOUNTRIES, chat_type='private')
    dp.register_callback_query_handler(registration_inProvinces, lambda c: c.data and c.data.startswith('start_provinces_'), state=StartStates.INPROVINCES, chat_type='private')
    dp.register_callback_query_handler(registration_inCities, lambda c: c.data and c.data.startswith('start_cities_'), state=StartStates.INCITIES, chat_type='private')
    dp.register_message_handler(registration_inSchools, state=StartStates.INSCHOOL, chat_type='private')
    dp.register_message_handler(registration_inClass, state=StartStates.INCLASS, chat_type='private')
    dp.register_message_handler(registration_inLogin, state=StartStates.INLOGIN, chat_type='private')
    dp.register_message_handler(registration_inPassword, state=StartStates.INPASSWORD, chat_type='private')



