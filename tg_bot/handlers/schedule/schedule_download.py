from database.methods.get import get_all_classes_by_school, get_chats_with_schedule_notification, get_schedule, get_student_by_telegram_id, get_students_with_schedule_notification
from database.methods.update import edit_schedule_photo, edit_student_telegram_id, edit_student_vk_id
from database.methods.create import create_schedule
from database.methods.delete import delete_chat


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
import aiogram

from vkbottle import Bot, VKAPIError

from .keyboard_schedule import keyboard_schedule
from tg_bot.utils import send_telegram_msg, send_telegram_bytes_photo
from tg_bot.keyboards.inline import kb_schedule_download, kb_back_to_schedule
from tg_bot.states import UpdScheduleStates

from vk_bot.utils import send_vk_msg

from settings import days_and_their_variations as days
from vk_bot.utils.send_vk_msg import send_vk_bytes_photo

from settings import vk_token, weekDays

import asyncio
import logging
import io


vk_bot = Bot(token=vk_token)

async def chat_start_schedule_download(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get schedule download request in chat')
    await callback.answer('❌Доступно только в л/с!')

async def private_start_schedule_download(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get schedule download request in private')
    await UpdScheduleStates.INPHOTO.set()
    await callback.message.edit_text('❓На какой день хотите загрузить расписание?')
    await callback.message.edit_reply_markup(reply_markup=kb_schedule_download)
    logging.info(f'{callback.message.chat.id}: I send schedule download question about day')

async def photo_schedule_download(callback: CallbackQuery, state: FSMContext):
    logging.info(f'{callback.message.chat.id}: I get schedule download day')
    day = callback.data.split('_')[2] # Получаем день недели
    day = [i for i in days if day in days[i]][0] # Получаем день недели в нужном формате
    if day in weekDays.values(): # Если день недели в нужном формате
        await state.update_data(day=day) # Обновляем данные
    else: # Если нет
        logging.info(f'{callback.message.chat.id}: I get schedule download day, but it is not a day')
        await callback.answer('❌Не нашел в вашем сообщении данные, нажмите еще раз') # Отвечаем, что не нашел день недели
        return
    await UpdScheduleStates.next() # Переходим к следующему шагу
    await callback.message.edit_text('📅Отправьте фото расписания')
    await callback.message.edit_reply_markup(reply_markup=kb_back_to_schedule)
    logging.info(f'{callback.message.chat.id}: I send schedule download question about photo')

async def class_schedule_download(message: Message, state: FSMContext):
    logging.info(f'{message.chat.id}:I get schedule download photo')
    photo: io.BytesIO = await message.bot.download_file_by_id(message.photo[-1].file_id) # Скачиваем фото в байтовом формате
    photo = photo.read()
    logging.info(f'{message.chat.id}: I save photo in bytes')

    await state.update_data(photo=photo) # Обновляем данные
    await UpdScheduleStates.next() # Переходим к следующему шагу
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Это расписание для всей школы', callback_data='ItsSheduleForAllSchool')).add(InlineKeyboardButton('↩️Назад', callback_data='keyboard_schedule'))
    await message.answer('❓Теперь отправьте класс, на который загружаете расписание', reply_markup=kb)
    logging.info(f'{message.chat.id}: I send schedule download question about class')

async def finish_schedule_download(message: Message, state: FSMContext):
    if isinstance(message, CallbackQuery): # Если получил CallbackQuery
        logging.info(f'{message.message.chat.id}: It is schedule for all school')
        message = message.message
        clas = 'all'
    else:
        clas = message.text.lower()
    logging.info(f'{message.chat.id}: I get schedule download class')
    all_data = await state.get_data() # Получаем все данные
    day = all_data['day']
    photo_as_bytes = all_data['photo']
    student = get_student_by_telegram_id(message.chat.id) # Получаем данные пользователя из БД
    school = student.school
    if clas == 'all': # Если расписание для всей школы
        for i in get_all_classes_by_school(school): # Перебираем все классы в этой школе
            if get_schedule(school, i[0], day) is None: # Если расписание не существует
                create_schedule(school, i[0], day, photo_as_bytes) # Создаем расписание
                logging.info(f'{message.chat.id}: I create schedule for {i[0]} class')
            else:
                edit_schedule_photo(school, i[0], day, photo_as_bytes) # Иначе редактируем расписание
                logging.info(f'{message.chat.id}: I edit schedule for {i[0]} class')
    else: # Если расписание для конкретного класса
        if get_schedule(school, clas, day) is None: # Если расписание не существует
            create_schedule(school, clas, day, photo_as_bytes) # Создаем расписание
            logging.info(f'{message.chat.id}: I create schedule for {clas} class')
        else:
            edit_schedule_photo(school, clas, day, photo_as_bytes) # Иначе редактируем расписание
            logging.info(f'{message.chat.id}: I edit schedule for {clas} class')
    
    await send_telegram_bytes_photo(bot=message.bot, chat_id=message.chat.id, photo=photo_as_bytes, caption=f'✅Расписание на {day} успешно обновлено!')
    logging.info(f'{message.chat.id}: I send schedule download success message')
    await state.finish() # Заканчиваем работу с FSM

    await keyboard_schedule(message) # Отправляем клавиатуру с расписанием

    # Начинаем рассылку расписания
    users_with_notification = get_students_with_schedule_notification()
    chats_with_notification = get_chats_with_schedule_notification()
    for i in users_with_notification: # Перебираем пользователей, которые подписаны на уведомления
        if i.school == school: # Если пользователь из этой школы
            if i.clas == clas or clas == 'all': # Если пользователь из этого класса или расписание для всей школы
                if i.vk_id: # Если у пользователя есть аккаунт ВК
                    try: # Пытаемся отправить расписание в ВК
                        await send_vk_bytes_photo(bot=vk_bot, photo=photo_as_bytes, user_id=i.vk_id, caption=f'🔄Новое расписание на {day}!')
                        logging.info(f'I send schedule to vk user. Id: {i.vk_id}')
                    except VKAPIError: # Если не получилось
                        logging.info(f'I can not send schedule to vk user. Id: {i.vk_id}')
                        if i.vk_id and i.telegram_id: # Если у пользователя есть аккаунт ВК и Телеграм
                            edit_student_vk_id(telegram_id=i.telegram_id, new_vk_id=None) # Удаляем аккаунт ВК
                            await send_telegram_msg(bot=message.bot, chat_id=i.telegram_id, text='❌Я не могу отправить вам сообщение в ВК, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в телеграмме')
                if i.telegram_id:
                    try: # Пытаемся отправить расписание в телеграмм
                        await send_telegram_bytes_photo(bot=message.bot, chat_id=i.telegram_id, caption=f'🔄Новое расписание на {day}!', photo=photo_as_bytes)
                        logging.info(f'I send schedule to telegram user. Id: {i.telegram_id}')
                    except aiogram.utils.exceptions.BotBlocked: # Если не получилось
                        logging.info(f'I can not send schedule to telegram user. Id: {i.telegram_id}')
                        if i.vk_id and i.telegram_id: # Если у пользователя есть аккаунт ВК и Телеграм
                            edit_student_telegram_id(vk_id=i.vk_id, new_telegram_id=None) # Удаляем аккаунт Телеграм
                            await send_vk_msg(bot=vk_bot, user_id=i.vk_id, message='❌Я не могу отправить вам сообщение в телеграмме, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в ВК')
                await asyncio.sleep(1)
    
    for i in chats_with_notification: # Перебираем чаты, которые подписаны на уведомления
        if i.school == school: # Если чат из этой школы
            if i.clas == clas or clas == 'all': # Если чат из этого класса или расписание для всей школы
                if i.vk_id:
                    try: # Пытаемся отправить расписание в ВК
                        await send_vk_bytes_photo(bot=vk_bot, photo=photo_as_bytes, chat_id=i.vk_id, caption=f'🔄Новое расписание на {day}!')
                        logging.info(f'I send schedule to vk chat. Id: {i.vk_id}')
                    except VKAPIError:  # Если не получилось
                        delete_chat(vk_id=i.vk_id) # Удаляем чат из базы данных
                        logging.info(f'I can not send schedule to vk chat and delete it. Id: {i.vk_id}')
                if i.telegram_id: # Если у пользователя есть аккаунт ВК и Телеграм
                    try: # Пытаемся отправить расписание в телеграмм
                        await send_telegram_bytes_photo(bot=message.bot, chat_id=i.telegram_id, caption=f'🔄Новое расписание на {day}!', photo=photo_as_bytes)
                        logging.info(f'I send schedule to telegram chat. Id: {i.telegram_id}')
                    except aiogram.utils.exceptions.BotKicked: # Если не получилось
                        delete_chat(telegram_id=i.telegram_id) # Удаляем чат из базы данных
                        logging.info(f'I can not send schedule to telegram chat and delete it. Id: {i.telegram_id}')
                await asyncio.sleep(1)
    logging.info(f'{message.chat.id}: I done mailing in schedule_download')







def register_schedule_download(dp: Dispatcher):
    dp.register_callback_query_handler(chat_start_schedule_download, lambda callback: callback.data == 'schedule_download', state='*', chat_type='group')
    dp.register_callback_query_handler(private_start_schedule_download, lambda callback: callback.data == 'schedule_download', state='*', chat_type='private')

    dp.register_callback_query_handler(photo_schedule_download, lambda callback: callback.data.startswith('update_schedule_'), state=UpdScheduleStates.INPHOTO)

    dp.register_message_handler(class_schedule_download, state=UpdScheduleStates.INCLASS, content_types=['photo'])

    dp.register_message_handler(finish_schedule_download, state=UpdScheduleStates.END, content_types=['text'])
    dp.register_callback_query_handler(finish_schedule_download, lambda callback: callback.data == 'ItsSheduleForAllSchool', state=UpdScheduleStates.END)