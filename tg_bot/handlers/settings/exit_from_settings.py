from aiogram.types import CallbackQuery
from aiogram import Dispatcher

import logging


async def exit_from_settings(callback: CallbackQuery): 
    logging.info(f'{callback.message.chat.id}: I get exit from settings command')   
    await callback.message.delete()
    logging.info(f'{callback.message.chat.id}: I delete settings keyboard')


def register_exit_from_settings_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(exit_from_settings, lambda c: c.data and c.data =='exit_from_settings')