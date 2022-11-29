from database.methods.get import get_chat_by_vk_id, get_homework, get_student_by_vk_id
from ns import get_diary, get_week
from settings import weekDays
import netschoolapi

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging
import datetime

bp = Blueprint('homework_for_day')# Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts




@bp.on.private_message(payload={'cmd': 'keyboard_homework_for_day'})
async def keyboard_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework_for_day')
    userId = message.from_id
    student = get_student_by_vk_id(userId)
    week = get_week()
    
    # Получаем дневник
    diary = await get_diary(
        student.login,
        student.password,
        week,
        student.school,
        student.link,
        student.studentId
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if (datetime.datetime.strptime(day['date'], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(diary['weekStart'], '%Y-%m-%dT%H:%M:%S')).days == i:
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
    chat = get_chat_by_vk_id(chatId)
    week = get_week()
    
    # Получаем дневник
    diary = await get_diary(
        chat.login,
        chat.password,
        week,
        chat.school,
        chat.link,
        chat.studentId
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if (datetime.datetime.strptime(day['date'], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(diary['weekStart'], '%Y-%m-%dT%H:%M:%S')).days == i:
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
    student = get_student_by_vk_id(userId)
    week = get_week() 
    day = int(message.payload[25:-2])

    try:
        diary = await get_diary( # Получаем дневник
            student.login,
            student.password,
            week,
            student.school,
            student.link,
            student.studentId
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return

    # Перебираем уроки
    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        # Получаем дз
        homework = get_homework(lesson, student.school, student.clas)
        if homework:
            await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
            logging.info(f'{message.peer_id}: Send homework')

    await message.answer('❗Внимание могут быть отправлены не все уроки. В этом случае рекомендуем вручную посмотреть Д/З по оставшимся урокам.')
    logging.info(f'{message.peer_id}: I send homework_for_day')





@bp.on.chat_message(PayloadStarts='{"cmd":"homework_for_day_')
async def chat_homework_for_day(message: Message):
    logging.info(f'{message.peer_id}: I get homework_for_day')
    chatId = message.chat_id # ID чата
    chat = get_chat_by_vk_id(chatId)
    week = get_week() 
    day = int(message.payload[25:-2])

    try:
        diary = await get_diary( # Получаем дневник
            chat.login,
            chat.password,
            week,
            chat.school,
            chat.link,
            chat.studentId
        )
        logging.info(f'{message.peer_id}: Get diary in NetSchool')
    except netschoolapi.errors.AuthError:
        await message.answer('❌Неправильный логин или пароль!')
        logging.info(f'{message.peer_id}: Incorrect login or password!')
        return

    # Перебираем уроки
    for lesson in diary['weekDays'][day]['lessons']:
        lesson = lesson['subjectName']

        # Получаем дз
        homework = get_homework(lesson, chat.school, chat.clas)
        if homework:
            await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {homework.upd_date} \n💬Задание: {homework.homework}')
            logging.info(f'{message.peer_id}: Send homework')

    await message.answer('❗Внимание могут быть отправлены не все уроки. В этом случае рекомендуем вручную посмотреть Д/З по оставшимся урокам.')
    logging.info(f'{message.peer_id}: I send homework_for_day')