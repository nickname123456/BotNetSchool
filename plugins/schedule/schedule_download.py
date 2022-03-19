from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
import logging
import asyncio
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD



bp = Blueprint('schedule_download') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр

db = SQLighter('database.db')# Подключаемся к базе данных

ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class ScheduleData(BaseStateGroup):
    DAY = 0
    PHOTO = 1
    SCHOOL = 2
    CLAS = 3



@bp.on.private_message(lev='/Загрузить')
async def day_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get /download')

    keyboard = (
        Keyboard()
        .add(Text('Понедельник'))
        .row()
        .add(Text('Вторник'))
        .row()
        .add(Text('Среда'))
        .row()
        .add(Text('Четверг'))
        .row()
        .add(Text('Пятница'))
    )

    await bp.state_dispenser.set(message.peer_id, ScheduleData.DAY) # Говорим, что следующий шаг - выбор дня
    await message.answer("На какой день?", keyboard=keyboard)


@bp.on.private_message(state=ScheduleData.DAY)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get day in schedule_download')
    ctx.set('day', message.text) # Загружаем во внутренне хранилище день недели
    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO) # Говорим, что следующий шаг - выбор фото
    await message.answer("Введи фото", keyboard=EMPTY_KEYBOARD)




@bp.on.private_message(state=ScheduleData.PHOTO)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get photo in schedule_download')
    ctx.set('photo', message.text) # Загружаем во внутренне хранилище фото
    await bp.state_dispenser.set(message.peer_id, ScheduleData.SCHOOL) # Говорим, что следующий шаг - выбор школы
    
    keyboard = (
        Keyboard()
        # Добавить кнопку
        .add(Text('МАОУ "СОШ № 47 г. Челябинска"'))
        # Новая строка
        .row()
        .add(Text('ФГКОУ «Волгоградский кадетский корпус...'))
    )

    await message.answer("Выбери школу", keyboard=keyboard)



@bp.on.private_message(state=ScheduleData.SCHOOL)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get school in schedule_download')
    ctx.set('school', message.text) # Загружаем во внутреннее хранилище школу
    await bp.state_dispenser.set(message.peer_id, ScheduleData.CLAS) # Говорим, что следующий шаг - выбор класса
    await message.answer('Введи класс', keyboard=EMPTY_KEYBOARD)




@bp.on.private_message(state=ScheduleData.CLAS)
async def finish_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get class in schedule_download')
    userInfo = await bp.api.users.get(message.from_id)
    user_id = userInfo[0].id
    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
    day = ctx.get('day') # Берем из хранилища день
    photo = ctx.get('photo') # Берем из хранилища фото
    school = ctx.get('school') # Берем из хранилища школу
    clas = message.text

    # Если день подходит по параматрам:
    if school == 'МАОУ "СОШ № 47 г. Челябинска"':
        school = 'МАОУ "СОШ № 47 г. Челябинска"'
    elif school == 'ФГКОУ «Волгоградский кадетский корпус...':
        school = 'ФГКОУ «Волгоградский кадетский корпус Следственного комитета Российской Федерации имени Ф.Ф. Слипченко»'
    else:
        await message.answer('Ошибка! Введена неправильная школа.')
        return

    if day in ['Понедельник','Вторник','Среда','Четверг','Пятница']:
        if 'photo-' in photo:
            db.edit_schedule(
                school,
                clas,
                day,
                photo) # Записать на этот день это фото
            db.commit()
        else:
            await message.answer('Ошибка! Введено неправильное фото.')
            return
    else:
        await message.answer('Ошибка! Введен неправильный день.')
        return

    await message.answer(f'{school}\n{clas}\n{day}\n{photo}', attachment={photo})

    users_with_notification = db.get_accounts_schedule_notification()
    chats_with_notification = db.get_chats_schedule_notification()
    for i in users_with_notification:
        i_id = i[0]
        if db.get_account_school(i_id) == school and db.get_account_class(i_id) == clas:
            await bp.api.messages.send(message='Новое расписание!', user_id=i_id, random_id=0, attachment=photo)
            await asyncio.sleep(1)

    for i in chats_with_notification:
        i_id = i[0]
        if db.get_chat_school(i_id) == school and db.get_chat_class(i_id) == clas:
            await bp.api.messages.send(message='Новое расписание!', peer_id=2000000000+i_id, random_id=0, attachment=photo)
            await asyncio.sleep(1)

    logging.info(f'{message.peer_id}: I sent success')
    return 'ура победа'
