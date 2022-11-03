from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import kb_schedule

async def keyboard_schedule(message: Message):
    if isinstance(message, CallbackQuery):
        message = message.message
    await message.answer("Выберите день недели", reply_markup=kb_schedule)



def register_schedule_handlers(dp: Dispatcher):
    dp.register_message_handler(keyboard_schedule, content_types=['text'], text=['расписание', '/расписание', '/hfcgbcfybt', '/расп', '/hfcg', '/rasp', 'скиньте расписание', 'дайте расписание'], state='*')
    dp.register_callback_query_handler(keyboard_schedule, lambda c: c.data == 'keyboard_schedule', state='*')