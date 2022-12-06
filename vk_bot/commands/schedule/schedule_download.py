from database.methods.get import get_all_classes_by_school, get_chats_with_schedule_notification, get_schedule, get_student_by_vk_id, get_students_with_schedule_notification
from database.methods.update import edit_schedule_photo, edit_student_telegram_id, edit_student_vk_id
from database.methods.create import create_schedule
from database.methods.delete import delete_chat

from vk_bot.commands.schedule.keyboard_schedule import keyboard_schedule
from tg_bot.utils import send_telegram_msg, send_telegram_bytes_photo
from vk_bot.utils import download_photo_as_bytes
from settings import weekDays, tg_token

from vkbottle import CtxStorage, BaseStateGroup, PhotoMessageUploader, VKAPIError
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

import aiogram

import logging
import asyncio

tg_bot = aiogram.Bot(token=tg_token, parse_mode='HTML')

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
    logging.info(f'{message.from_id}: I get command shedule_download in chat')
    await message.answer("❌Доступно только в л/с!")

@bp.on.message(payload={'cmd': 'schedule_download'})
@bp.on.private_message(text=['/загрузить расписание', '/загрузить расп', '/лоадрасп', '/loadshedule'])
async def start_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get command shedule_download in private')

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
        .add(Text('Назад', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO) # Говорим, что следующий шаг - выбор фото
    await message.answer("❓На какой день хотите загрузить расписание?", keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send question about day')


@bp.on.private_message(state=ScheduleData.PHOTO)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get day in schedule_download')
    if message.text in weekDays.values(): # Проверяем, что юзер ввел день недели
        ctx.set('day', message.text) # Загружаем во внутренне хранилище день недели
    elif message.text.lower() == 'назад':
        await keyboard_schedule(message)
        return
    else:
        logging.info(f'{message.peer_id}: I get wrong day in schedule_download')
        await message.answer('❌Не нашел в вашем сообщении данные, введите еще раз')
        return
    await bp.state_dispenser.set(message.peer_id, ScheduleData.CLAS) # Говорим, что следующий шаг - выбор класса
    keyboard = ( # Создаем клавиатуру с кнопкой назад
        Keyboard()
        .add(Text('Назад', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.NEGATIVE)
    )
    await message.answer("📅Отправьте фото расписания", keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send question about photo')


@bp.on.private_message(state=ScheduleData.CLAS)
async def class_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get photo in schedule_download')

    if message.attachments and message.attachments[0].photo: # Проверяем, что юзер отправил фото
        photo = message.attachments[0].photo
    elif message.text.lower() == 'назад':
        await keyboard_schedule(message)
        return
    else:
        logging.info(f'{message.peer_id}: I get wrong photo in schedule_download')
        await message.answer('❌Не нашел в вашем сообщении фото, отправьте еще раз')
        return
    ctx.set('photo', download_photo_as_bytes(photo)) # Загружаем во внутренне хранилище фото
    await bp.state_dispenser.set(message.peer_id, ScheduleData.FINISH)

    keyboard = (
        Keyboard()
        .add(Text('Это расписание для всей школы', {'LoadShedule': 'ItsSheduleForAllSchool'}), color=KeyboardButtonColor.SECONDARY)
    )

    await message.answer("❓Теперь отправьте класс, на который загружаете расписание", keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send question about class')


@bp.on.private_message(state=ScheduleData.FINISH)
async def finish_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get finish in schedule_download')
    userId = message.from_id # ID юзера
    student = get_student_by_vk_id(userId)

    day = ctx.get('day')
    photo_as_bytes = ctx.get('photo')
    photo = await PhotoMessageUploader(api=message.ctx_api).upload(photo_as_bytes) # Загружаем фото на сервера ВК
    school = student.school
    if message.text == 'Это расписание для всей школы': # Если расписание для всей школы
        for i in get_all_classes_by_school(student.school): # Перебираем все классы
            clas = i[0]
            if get_schedule(school, clas, day) is None: # Если расписание не загружено
                create_schedule(school, clas, day, photo_as_bytes) # Загружаем расписание
                logging.info(f'{message.peer_id}: I create schedule for {clas}')
            else: # Если расписание загружено
                edit_schedule_photo(school, clas, day, photo_as_bytes) # Заменяем фото
                logging.info(f'{message.peer_id}: I edit schedule for {clas}')
        clas = 'all'

    else: # Если расписание для конкретного класса
        clas = message.text.lower() 

        if get_schedule(school, clas, day) is None: # Если расписание не загружено
            create_schedule(school, clas, day, photo_as_bytes) # Загружаем расписание
            logging.info(f'{message.peer_id}: I create schedule for {clas}')
        else: # Если расписание загружено
            edit_schedule_photo(school, clas, day, photo_as_bytes) # Заменяем фото
            logging.info(f'{message.peer_id}: I edit schedule for {clas}')

    await message.answer('✅Расписание успешно обновлено!', attachment=photo)
    await bp.state_dispenser.delete(message.from_id) # Удаляем цепочку состояний
    logging.info(f'{message.peer_id}: I send success message and delete state')

    await keyboard_schedule(message) # Переносим юзера в меню расписания

    users_with_notification = get_students_with_schedule_notification() # Получаем всех юзеров, которые подписаны на уведомления
    chats_with_notification = get_chats_with_schedule_notification() # Получаем все чаты, которые подписаны на уведомления
    for i in users_with_notification: # Перебираем всех юзеров
        if i.school == school: # Если школа совпадает
            if i.clas == clas or clas == 'all': # Если класс совпадает или расписание для всей школы
                if i.vk_id: # Если есть аккаунт ВК
                    try: # Пытаемся отправить уведомление
                        await bp.api.messages.send(message=f'🔄Новое расписание на {day}!', user_id=i.vk_id, random_id=0, attachment=photo)
                        logging.info(f'{i.vk_id}: I send schedule notification')
                    except VKAPIError: # Если не получилось
                        logging.info(f'{i.vk_id}: I cant send schedule notification')
                        if i.vk_id and i.telegram_id: # Если есть аккаунт ВК и Телеграм
                            edit_student_vk_id(telegram_id=i.telegram_id, new_vk_id=None) # Удаляем аккаунт ВК
                            await send_telegram_msg(bot=tg_bot, chat_id=i.telegram_id, text='❌Я не могу отправить вам сообщение в ВК, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в телеграмме')
                if i.telegram_id: # Если есть аккаунт Телеграм
                    try: # Пытаемся отправить уведомление
                        await send_telegram_bytes_photo(bot=tg_bot, chat_id=i.telegram_id, caption=f'🔄Новое расписание на {day}!', photo=photo_as_bytes)
                        logging.info(f'{i.telegram_id}: I send schedule notification')
                    except aiogram.utils.exceptions.BotBlocked: # Если не получилось
                        logging.info(f'{i.telegram_id}: I cant send schedule notification')
                        if i.vk_id and i.telegram_id: # Если есть аккаунт ВК и Телеграм
                            edit_student_telegram_id(vk_id=i.vk_id, new_telegram_id=None) # Удаляем аккаунт Телеграм
                            await bp.api.messages.send(message='❌Я не могу отправить вам сообщение в телеграмме, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в ВК', user_id=i.vk_id, random_id=0)
                await asyncio.sleep(1)

    for i in chats_with_notification: # Перебираем все чаты
        if i.school == school: # Если школа совпадает
            if i.clas == clas or clas == 'all': # Если класс совпадает или расписание для всей школы
                if i.vk_id: # Если есть аккаунт ВК
                    try: # Пытаемся отправить уведомление
                        await bp.api.messages.send(message=f'🔄Новое расписание на {day}!', peer_id=2000000000+i.vk_id, random_id=0, attachment=photo)
                        logging.info(f'{2000000000+i.vk_id}: I send schedule notification')
                    except VKAPIError: # Если не получилось
                        delete_chat(vk_id=i.vk_id) # Удаляем чат
                        logging.info(f'{2000000000+i.vk_id}: I cant send schedule notification and delete chat')
                if i.telegram_id: # Если есть аккаунт Телеграм
                    try: # Пытаемся отправить уведомление
                        await send_telegram_bytes_photo(bot=tg_bot, chat_id=i.telegram_id, caption=f'🔄Новое расписание на {day}!', photo=photo_as_bytes)
                        logging.info(f'{i.telegram_id}: I send schedule notification')
                    except aiogram.utils.exceptions.BotKicked: # Если не получилось
                        delete_chat(telegram_id=i.telegram_id) # Удаляем чат
                        logging.info(f'{i.telegram_id}: I cant send schedule notification and delete chat')
                await asyncio.sleep(1)
    logging.info(f'{message.peer_id}: I done mailing in schedule_download')