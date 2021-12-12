from ns import get_back_period, get_next_period, get_period, get_diary
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
import netschoolapi
from settings import admin_login, admin_password, admin_link, admin_school




bp = Blueprint('homework')
db = SQLighter('database.db')




@bp.on.private_message(payload={'cmd': 'homework'})
async def keyboard_schedule(message: Message):
    userInfo = await bp.api.users.get(message.from_id)
    
    homework = db.get_homework(
        db.get_account_school(userInfo[0].id),
        db.get_account_class(userInfo[0].id),
        message.text
    )

    upd_date = db.get_upd_date(
        db.get_account_school(userInfo[0].id),
        db.get_account_class(userInfo[0].id),
        message.text
    )

    await message.answer(f'Урок: {message.text} \nБыло обновлено: {upd_date} \nЗадание: {homework}')



@bp.on.chat_message(payload={'cmd': 'homework'})
async def keyboard_schedule(message: Message):
    chat_id = message.chat_id

    homework = db.get_homework(
        db.get_chat_school(chat_id),
        db.get_chat_class(chat_id),
        message.text[33:]
    )

    upd_date = db.get_upd_date(
        db.get_chat_school(chat_id),
        db.get_chat_class(chat_id),
        message.text[33:]
    )

    await message.answer(f'Урок: {message.text[33:]} \nБыло обновлено: {upd_date} \nЗадание: {homework}')
