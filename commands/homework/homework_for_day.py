from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging
from PostgreSQLighter import db
from ns import get_diary, get_week
import netschoolapi
from settings import lessons_and_their_reduction
from settings import weekDays
from VKRules import PayloadStarts


bp = Blueprint('homework_for_day')# Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts




@bp.on.private_message(payload={'cmd': 'keyboard_homework_for_day'})
async def keyboard_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework_for_day')
    userId = message.from_id
    week = get_week()
    
    # Получаем дневник
    diary = await get_diary(
        db.get_account_login(userId),
        db.get_account_password(userId),
        week,
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId)
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"homework_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой день хотите узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework_for_day')

@bp.on.chat_message(payload={'cmd': 'keyboard_homework_for_day'})
async def keyboard_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework_for_day')
    chatId = message.chat_id
    week = get_week()
    
    # Получаем дневник
    diary = await get_diary(
        db.get_chat_login(chatId),
        db.get_chat_password(chatId),
        week,
        db.get_chat_school(chatId),
        db.get_chat_link(chatId),
        db.get_chat_studentId(chatId)
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"homework_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой день хотите узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework_for_day')





@bp.on.private_message(PayloadStarts='{"cmd":"homework_for_day_')
async def private_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    userId = message.from_id # ID юзера
    week = get_week() 
    day = int(message.payload[25:-2])

    try:
        diary = await get_diary( # Получаем дневник
            db.get_account_login(userId),
            db.get_account_password(userId),
            week,
            db.get_account_school(userId),
            db.get_account_link(userId),
            db.get_account_studentId(userId)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return

    # Перебираем уроки
    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        if lesson in lessons_and_their_reduction: lesson = lessons_and_their_reduction[lesson]

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
        except:
            logging.exception(f'{message.peer_id}: Exception occurred')
            continue

        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    await message.answer('❗Внимание могут быть отправлены не все уроки. В этом случае рекомендуем вручную посмотреть Д/З по оставшимся урокам.')
    logging.info(f'{message.peer_id}: I send homework_for_day')





@bp.on.chat_message(PayloadStarts='{"cmd":"homework_for_day_')
async def chat_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    chatId = message.chat_id # ID юзера
    week = get_week() 
    day = int(message.payload[25:-2])

    try:
        diary = await get_diary( # Получаем дневник
            db.get_chat_login(chatId),
            db.get_chat_password(chatId),
            week,
            db.get_chat_school(chatId),
            db.get_chat_link(chatId),
            db.get_chat_studentId(chatId)
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return

    # Перебираем уроки
    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        if lesson in lessons_and_their_reduction: lesson = lessons_and_their_reduction[lesson]

        try:
            # Получаем дз
            homework = db.get_homework(
                db.get_chat_school(chatId),
                db.get_chat_class(chatId),
                lesson
            )

            # Получаем дату обновления дз
            upd_date = db.get_upd_date(
                db.get_chat_school(chatId),
                db.get_chat_class(chatId),
                lesson
            )
        except:
            logging.exception(f'{message.peer_id}: Exception occurred')
            continue

        await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
        logging.info(f'{message.peer_id}: Send homework')

    await message.answer('❗Внимание могут быть отправлены не все уроки. В этом случае рекомендуем вручную посмотреть Д/З по оставшимся урокам.')
    logging.info(f'{message.peer_id}: I send homework_for_day')