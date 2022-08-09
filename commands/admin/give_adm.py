from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
from settings import ADM_PASSWORD



bp = Blueprint('give_admin')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=[ADM_PASSWORD])
async def give_admin(message: Message, userId=None):
    logging.info(f'{message.peer_id}: I get give_admin')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if db.get_account_isAdmin(user_id) == 1:
        db.edit_account_isAdmin(user_id, 0)
        await message.answer('У тебя уже есть админка! Ну хорошо, я ее с тебя снимаю')
        return
    
    db.edit_account_isAdmin(user_id, 1)
    await message.answer('Поздравляю! У тебя теперь есть админка!')
