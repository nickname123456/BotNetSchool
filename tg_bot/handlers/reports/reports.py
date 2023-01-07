from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import kb_reports

import logging


async def reports(message: Message, callback=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = message.message
    logging.info(f'{message.chat.id}: get report command')

    if callback:
        message.edit_text('✅Вот доступные отчеты:')
        message.edit_reply_markup(reply_markup=kb_reports)
    else:
        await message.answer('✅Вот доступные отчеты:', reply_markup=kb_reports)
    logging.info(f'{message.chat.id}: I sent reports')


def register_handlers_reports(dp: Dispatcher):
    dp.register_message_handler(reports, content_types=['text'], text_startswith=['отчеты', 'Отчеты', '📄Отчеты'], state='*')
    dp.register_message_handler(reports, commands='reports', state='*')
    dp.register_callback_query_handler(reports, lambda c: c.data == 'reports', state='*')