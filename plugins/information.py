from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import getSettings


bp = Blueprint('information')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр

db = SQLighter('database.db')# Подключаемся к базеданных


#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.private_message(payload={'cmd': 'information'})
async def private_information(message: Message):
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    result= await getSettings(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id)
    )
    await message.answer(result)





#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.chat_message(payload={'cmd': 'information'})
async def chat_information(message: Message):
    # Айди чата:
    chat_id = message.chat_id

    result= await getSettings(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id)
    )
    await message.answer(result)