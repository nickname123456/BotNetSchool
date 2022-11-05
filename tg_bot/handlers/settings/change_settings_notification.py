from database.methods.update import switch_chat_announcements_notification, switch_chat_homework_notification, switch_chat_mark_notification, switch_chat_schedule_notification, switch_student_announcements_notification, switch_student_homework_notification, switch_student_mark_notification, switch_student_schedule_notification
from database.methods.get import get_chat_by_telegram_id, get_student_by_telegram_id
from tg_bot.keyboards import get_settings_kb

from aiogram.types import CallbackQuery
from aiogram import Dispatcher

import logging


async def switch_mark_notification_private(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch mark notification command')
    user_id = callback.message.chat.id

    switch_student_mark_notification(telegram_id=user_id)

    kb = get_settings_kb(
        get_student_by_telegram_id(user_id)
    )
    
    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch mark notification')


async def switch_mark_notification_chat(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch mark notification command')
    chat_id = callback.message.chat.id

    switch_chat_mark_notification(telegram_id=chat_id)

    kb = get_settings_kb(
        get_chat_by_telegram_id(chat_id)
    )

    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch mark notification')


async def switch_schedule_notification_private(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch schedule notification command')
    user_id = callback.message.chat.id

    switch_student_schedule_notification(telegram_id=user_id)

    kb = get_settings_kb(
        get_student_by_telegram_id(user_id)
    )
    
    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch schedule notification')


async def switch_schedule_notification_chat(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch schedule notification command')
    chat_id = callback.message.chat.id

    switch_chat_schedule_notification(telegram_id=chat_id)

    kb = get_settings_kb(
        get_chat_by_telegram_id(chat_id)
    )

    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch schedule notification')


async def switch_announcements_notification_private(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch announcements notification command')
    user_id = callback.message.chat.id

    switch_student_announcements_notification(telegram_id=user_id)

    kb = get_settings_kb(
        get_student_by_telegram_id(user_id)
    )
    
    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch announcements notification')


async def switch_announcements_notification_chat(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch announcements notification command')
    chat_id = callback.message.chat.id

    switch_chat_announcements_notification(telegram_id=chat_id)

    kb = get_settings_kb(
        get_chat_by_telegram_id(chat_id)
    )

    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch announcements notification')


async def switch_homework_notification_private(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch homework notification command')
    user_id = callback.message.chat.id

    switch_student_homework_notification(telegram_id=user_id)

    kb = get_settings_kb(
        get_student_by_telegram_id(user_id)
    )
    
    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch homework notification')


async def switch_homework_notification_chat(callback: CallbackQuery):
    logging.info(f'{callback.message.chat.id}: I get switch homework notification command')
    chat_id = callback.message.chat.id

    switch_chat_homework_notification(telegram_id=chat_id)

    kb = get_settings_kb(
        get_chat_by_telegram_id(chat_id)
    )

    await callback.answer('✅Изменения приняты!')
    await callback.message.edit_reply_markup(reply_markup=kb)
    logging.info(f'{callback.message.chat.id}: I switch homework notification')



def register_change_settings_notification_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(switch_mark_notification_private, lambda c: c.data and c.data =='change_mark_notification', chat_type='private')
    dp.register_callback_query_handler(switch_mark_notification_chat, lambda c: c.data and c.data =='change_mark_notification', chat_type='group')

    dp.register_callback_query_handler(switch_schedule_notification_private, lambda c: c.data and c.data =='change_schedule_notification', chat_type='private')
    dp.register_callback_query_handler(switch_schedule_notification_chat, lambda c: c.data and c.data =='change_schedule_notification', chat_type='group')

    dp.register_callback_query_handler(switch_announcements_notification_private, lambda c: c.data and c.data =='change_announcements_notification', chat_type='private')
    dp.register_callback_query_handler(switch_announcements_notification_chat, lambda c: c.data and c.data =='change_announcements_notification', chat_type='group')

    dp.register_callback_query_handler(switch_homework_notification_private, lambda c: c.data and c.data =='change_homework_notification', chat_type='private')
    dp.register_callback_query_handler(switch_homework_notification_chat, lambda c: c.data and c.data =='change_homework_notification', chat_type='group')