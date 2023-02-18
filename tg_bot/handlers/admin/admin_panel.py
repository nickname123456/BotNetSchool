from database.methods.get import get_all_chats, get_all_homeworks, get_all_schedules, get_all_students, get_student_by_telegram_id, get_students_with_admin

from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import admin_kb
# from settings import reduction_for_search

import logging


async def admin_panel(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = callback.message
    user_id = message.chat.id
    logging.info(f'{user_id}: I get admin panel')

    student = get_student_by_telegram_id(user_id)
    if not student.isAdmin:
        await message.answer('❌У тебя нет админских прав!')
        return

    await message.answer("👹Ты в админ панели.", reply_markup=admin_kb)

    logging.info(f'{user_id}: I sent admin panel')


async def admin_stats(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get admin stats')
    message = callback.message
    user_id = message.chat.id

    student = get_student_by_telegram_id(user_id)
    if not student.isAdmin:
        await message.edit_text('❌У тебя нет админских прав!')
        return



    admins = get_students_with_admin()  # Все админы
    num_admins = len(admins)  # Кол-во админов
    admins_vk_id = [admin.vk_id for admin in admins]  # IDшники админов
    admins_tg_id = [admin.telegram_id for admin in admins]  # IDшники админов

    all_users = get_all_students()
    all_chats = get_all_chats()
    num_users = len(all_users)  # Кол-во пользователей
    num_chats = len(all_chats)  # Кол-во чатов

    num_schedule = len(get_all_schedules())  # Кол-во расписаний
    num_homework = len(get_all_homeworks())  # Кол-во домашек

    regions = []
    schools = []
    num_users_from_chel = 0
    num_users_from_47 = 0
    for user in all_users:
        if user.school not in schools:
            schools.append(user.school)

        if user.link not in regions:
            regions.append(user.link)

        if user.link.startswith('https://sgo.edu-74.ru'):
            num_users_from_chel += 1

        if user.school == 'МАОУ "СОШ № 47 г. Челябинска"':
            num_users_from_47 += 1

    num_regions = len(regions)  # Кол-во регионов
    num_schools = len(schools)  # Кол-во школ

    await message.edit_text(f"""
🤡Число админов: {num_admins}
ID'шники админов в ТГ: {admins_tg_id}
ID'шники админов в ВК: {admins_vk_id}
====================
🦣Число пользователей: {num_users}
👨‍👨‍👦‍👦Число чатов: {num_chats}
====================
📅Число расписаний: {num_schedule}
📚Число домашек: {num_homework}
====================
🌍Число регионов: {num_regions}
🏠Число пользователей из Челябинска: {num_users_from_chel}
====================
🏫Число школ: {num_schools}
👨‍🏫Число пользователей из твоей шк: {num_users_from_47}
""", reply_markup=admin_kb)

    logging.info(f'{user_id}: I sent admin stats')




# async def admin_search_banner(message: Message, callback=None):
#     if isinstance(message, CallbackQuery):
#         callback = message
#         message = callback.message
#     user_id = message.chat.id
#     logging.info(f'{user_id}: I get admin search')

#     student = get_student_by_telegram_id(user_id)
#     if not student.isAdmin:
#         await message.answer('❌У тебя нет админских прав!')
#         return

#     if message.from_user.id == user_id and message.text.startswith('/search') and message.text != '/search':
#         await admin_search(message)
#     else:
#         await message.answer("💡Используй /search {ОБЪЕКТ} {сокращение=значение}", reply_markup=admin_kb)
#         await message.answer("""
# Сокращения:
# ЮЗЕР - пользователь
# ЧАТ - чат
# ДЗ - домашнее задание
# РАСП - расписание

# ИД - id
# АДМ - isAdmin
# ВКИД - vk_id
# ТГИД - telegram_id
# ЛОГИН - login
# ПАСС - password
# ЛИНК - link
# СКУЛ - school
# КЛАСС - class
# СТУДИД - student_id
# МАРКНОТИФ - mark_notification
# ХОМНОТИФ - homework_notification
# ОЛДМАРК- old_mark
# ОЛДАНОНЦ - old_announcements
# КОРЛЕССОН - correction_lesson
# КОРМАРК - correction_mark
# КОННЕКТ - connect_code
# """)
#     logging.info(f'{user_id}: I sent admin search')
    
# async def admin_search (message: Message):
#     user_id = message.chat.id
#     logging.info(f'{user_id}: I get admin search')
#     student = get_student_by_telegram_id(user_id)
#     if not student.isAdmin:
#         await message.answer('❌У тебя нет админских прав!')
#         return
    
#     args = message.text.split(' ')[1:]
#     obj = reduction_for_search[args[0]]
#     arg, value = args[1].split('=')
#     arg = reduction_for_search[arg]


#     await message.answer(f'🔎Ищу {args}')
    
    




def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, content_types=['text'], text=[
                                "админ", 'админка', 'flvby', 'admin', "/админ", '/админка', '/flvby', '/admin'], state='*', chat_type='private')
    dp.register_callback_query_handler(
        admin_panel, lambda c: c.data == 'admin_panel', state='*', chat_type='private')

    dp.register_callback_query_handler(admin_stats, lambda c: c.data == 'admin_stats', state='*', chat_type='private')

    # dp.register_message_handler(admin_search_banner, content_types=['text'], text=['/search'], state='*', chat_type='private')
    # dp.register_message_handler(admin_search_banner, commands=['search'], state='*', chat_type='private')
    # dp.register_callback_query_handler(admin_search_banner, lambda c: c.data == 'admin_search', state='*', chat_type='private')