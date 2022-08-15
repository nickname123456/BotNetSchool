from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from PostgreSQLighter import db
from ns import get_diary, get_week
import netschoolapi
from settings import lessons_and_their_reduction


bp = Blueprint('homework_for_day')# Объявляем команду




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

    await message.answer('🤔На какой день хотите узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework_for_day')





@bp.on.private_message(payload={'cmd': 'homework_for_day'})
async def private_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    userId = message.from_id # ID юзера
    
    #Если логин или пароль не правильнй
    if db.get_account_correctData(userId) != 1:
        await message.answer('❌Вы не зарегистрированы! \nНапишите "Начать"\n ❌Или у вас неверный логин/пароль')
        logging.info(f'{message.peer_id}: User not found in db')
        return

    try:
        diary = await get_diary( # Получаем дневник
            db.get_account_login(userId),
            db.get_account_password(userId),
            get_week(),
            db.get_account_school(userId),
            db.get_account_link(userId),
            db.get_account_studentId(userId)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
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

    # Перебираем уроки
    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']
        if lesson == 'Проектная деятельность':
            continue
        lesson = lessons_and_their_reduction[lesson]
        try:
            # Получаем дз
            homework = db.get_homework(
                db.get_account_school(userId),
                db.get_account_class(userId),
                lesson
            )

            # Получаем дату обновления дз
            upd_date = db.get_upd_date(
                db.get_account_school(userId),
                db.get_account_class(userId),
                lesson
            )
        except TypeError:
            logging.exception(f'{message.peer_id}: Exception occurred')
            await message.answer('❌Вы не зарегистрированы! \nНапишите "Начать"\n ❌Или у вас неверный логин/пароль')
            return

        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    logging.info(f'{message.peer_id}: I send homework_for_day')





@bp.on.chat_message(payload={'cmd': 'homework_for_day'})
async def chat_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    chat_id = message.chat_id

    try:
        diary = await get_diary( # Получаем дневник
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            get_week(),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_studentId(chat_id)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
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

    # Перебираем уроки
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
            await message.answer('❌Вы не зарегистрированы! \nНапишите "Начать"\n ❌Или у вас неверный логин/пароль')
            return

        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    logging.info(f'{message.peer_id}: I send homework_for_day')