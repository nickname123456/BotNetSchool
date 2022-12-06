from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from tg_bot.keyboards import kb_schedule

async def keyboard_schedule(message: Message, callback: CallbackQuery=None):
    if isinstance(message, CallbackQuery):
        callback = message
        message = callback.message

    if callback:
        await message.edit_text('Выберите день недели.')
        await message.edit_reply_markup(kb_schedule)
    else:
        await message.answer("Выберите день недели", reply_markup=kb_schedule)



def register_schedule_handlers(dp: Dispatcher):
    dp.register_message_handler(keyboard_schedule, content_types=['text'], text=['расписание', '/расписание', '/hfcgbcfybt', '/расп', '/hfcg', '/rasp', 'скиньте расписание', 'дайте расписание', '📚Расписание'], state='*')
    dp.register_message_handler(keyboard_schedule, commands=['schedule'], state='*')
    dp.register_callback_query_handler(keyboard_schedule, lambda c: c.data == 'keyboard_schedule', state='*')