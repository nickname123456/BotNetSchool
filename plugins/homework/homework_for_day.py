import imp
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
import logging
from sqlighter import SQLighter
from ns import get_diary, get_period
import netschoolapi
from settings import lessons_and_their_reduction


bp = Blueprint('homework_for_day')# Объявляем команду
db = SQLighter('database.db') # Подключаемся к базеданных




@bp.on.message(payload={'cmd': 'keyboard_homework_for_day'})
async def keyboard_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework_for_day')
    keyboard = (
        Keyboard()
        .add(Text('Понедельник', {"cmd": "homework_for_day"}))
        .row()
        .add(Text('Вторник', {'cmd': 'homework_for_day'}))
        .row()
        .add(Text('Среда', {'cmd': 'homework_for_day'}))
        .row()
        .add(Text('Четверг', {'cmd': 'homework_for_day'}))
        .row()
        .add(Text('Пятница', {'cmd': 'homework_for_day'}))
        .row()
        .add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('На какой день хочешь узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework_for_day')





@bp.on.private_message(payload={'cmd': 'homework_for_day'})
async def private_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    
    #Если дневника нет в списке
    if db.get_account_correctData(userInfo[0].id) != 1:
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        logging.info(f'{message.peer_id}: User not found in db')
        return

    try:
        diary = await get_diary(
            db.get_account_login(userInfo[0].id),
            db.get_account_password(userInfo[0].id),
            get_period(),
            db.get_account_school(userInfo[0].id),
            db.get_account_link(userInfo[0].id)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return
    
    if 'Понедельник' in message.text:
        day = 0
    elif 'Вторник' in message.text:
        day = 1
    elif 'Среда' in message.text:
        day = 2
    elif 'Четверг' in message.text:
        day = 3
    elif 'Пятница' in message.text:
        day = 4

    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']
        lesson = lessons_and_their_reduction[lesson]
        try:
            # Получаем дз
            homework = db.get_homework(
                db.get_account_school(userInfo[0].id),
                db.get_account_class(userInfo[0].id),
                lesson
            )

            # Получаем дату обновления дз
            upd_date = db.get_upd_date(
                db.get_account_school(userInfo[0].id),
                db.get_account_class(userInfo[0].id),
                lesson
            )
        except TypeError:
            logging.exception(f'{message.peer_id}: Exception occurred')
            await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
            return

        await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    logging.info(f'{message.peer_id}: I send homework_for_day')





@bp.on.chat_message(payload={'cmd': 'homework_for_day'})
async def chat_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    chat_id = message.chat_id

    try:
        diary = await get_diary(
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            get_period(),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return
    
    if 'Понедельник' in message.text:
        day = 0
    elif 'Вторник' in message.text:
        day = 1
    elif 'Среда' in message.text:
        day = 2
    elif 'Четверг' in message.text:
        day = 3
    elif 'Пятница' in message.text:
        day = 4

    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']
        lesson = lessons_and_their_reduction[lesson]
        try:
            # Получаем дз
            homework = db.get_homework(
                db.get_chat_school(chat_id),
                db.get_chat_class(chat_id),
                lesson
            )

            # Получаем дату обновления дз
            upd_date = db.get_upd_date(
                db.get_chat_school(chat_id),
                db.get_chat_class(chat_id),
                lesson
            )
        except TypeError:
            logging.exception(f'{message.peer_id}: Exception occurred')
            await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
            return

        await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    logging.info(f'{message.peer_id}: I send homework_for_day')