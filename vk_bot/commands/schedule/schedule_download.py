from database.methods.get import get_all_classes_by_school, get_chats_with_schedule_notification, get_schedule, get_student_by_vk_id, get_students_with_schedule_notification
from database.methods.update import edit_schedule_photo
from database.methods.create import create_schedule

from vk_bot.commands.schedule.keyboard_schedule import keyboard_schedule
from settings import weekDays

from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle import CtxStorage, BaseStateGroup
from vkbottle.bot import Message, Blueprint

import logging
import asyncio


bp = Blueprint('schedule_download') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class ScheduleData(BaseStateGroup):
    PHOTO = 1
    CLAS = 2
    FINISH = 3

@bp.on.chat_message(payload={'cmd': 'schedule_download'})
@bp.on.chat_message(text=['/загрузить расписание', '/загрузить расп', '/лоадрасп', '/loadshedule'])
async def start_schedule_download(message: Message):
    await message.answer("❌Доступно только в л/с!")

@bp.on.message(payload={'cmd': 'schedule_download'})
@bp.on.private_message(text=['/загрузить расписание', '/загрузить расп', '/лоадрасп', '/loadshedule'])
async def start_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get /loadshedule')

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
        .row()
        .add(Text('Суббота'))
        .row()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO) # Говорим, что следующий шаг - выбор фото
    await message.answer("❓На какой день хотите загрузить расписание?", keyboard=keyboard)


@bp.on.private_message(state=ScheduleData.PHOTO)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get day in schedule_download')
    if message.text in weekDays.values():
        ctx.set('day', message.text) # Загружаем во внутренне хранилище день недели
    else:
        await message.answer('❌Не нашел в вашем сообщении данные, введите еще раз')
        return
    await bp.state_dispenser.set(message.peer_id, ScheduleData.CLAS) # Говорим, что следующий шаг - выбор класса
    await message.answer("📅Отправьте фото расписания", keyboard=EMPTY_KEYBOARD)


@bp.on.private_message(state=ScheduleData.CLAS)
async def class_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get itsmyschool in schedule_download')

    if message.attachments and message.attachments[0].photo:
        photo = message.attachments[0].photo
    else:
        await message.answer('❌Не нашел в вашем сообщении фото, отправьте еще раз')
        return
    ctx.set('photo', f'photo{photo.owner_id}_{photo.id}_{photo.access_key}') # Загружаем во внутренне хранилище фото
    await bp.state_dispenser.set(message.peer_id, ScheduleData.FINISH)

    keyboard = (
        Keyboard()
        .add(Text('Это расписание для всей школы', {'LoadShedule': 'ItsSheduleForAllSchool'}), color=KeyboardButtonColor.SECONDARY)
    )

    await message.answer("❓Теперь отправь класс, на который загружаешь расписание", keyboard=keyboard)


@bp.on.private_message(state=ScheduleData.FINISH)
async def finish_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get finish in schedule_download')
    userId = message.from_id # ID юзера
    student = get_student_by_vk_id(userId)

    day = ctx.get('day')
    photo = ctx.get('photo')
    school = student.school
    if message.text == 'Это расписание для всей школы':
        for i in get_all_classes_by_school(student.school):
            clas = i[0]
            if get_schedule(school, clas, day) is None:
                create_schedule(school, clas, day, photo)
            else:
                edit_schedule_photo(school, clas, day, photo)
        clas = 'all'

    else: 
        clas = message.text.lower()

        if get_schedule(school, clas, day) is None:
            create_schedule(school, clas, day, photo)
        else:
            edit_schedule_photo(school, clas, day, photo)

    await message.answer('✅Расписание успешно обновлено!', attachment=photo)
    await bp.state_dispenser.delete(message.from_id)

    await keyboard_schedule(message)

    users_with_notification = get_students_with_schedule_notification()
    chats_with_notification = get_chats_with_schedule_notification()
    for i in users_with_notification:
        if i.school == school:
            if i.clas == clas or clas == 'all':
                await bp.api.messages.send(message='🔄Новое расписание!', user_id=i.vk_id, random_id=0, attachment=photo)
                await asyncio.sleep(1)

    for i in chats_with_notification:
        if i.school == school:
            if i.clas == clas or clas == 'all':
                await bp.api.messages.send(message='🔄Новое расписание!', peer_id=2000000000+i.vk_id, random_id=0, attachment=photo)
                await asyncio.sleep(1)
    logging.info(f'{message.peer_id}: I sent success')