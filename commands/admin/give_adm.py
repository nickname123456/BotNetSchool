from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging
from settings import ADM_PASSWORD # Пароль для получения админки



bp = Blueprint('give_admin')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=[ADM_PASSWORD])
async def give_admin(message: Message):
    logging.info(f'{message.peer_id}: I get give_admin')
    user_id = message.from_id  # ID юзера

    # Проверка на админа
    if db.get_account_isAdmin(user_id) == 1:
        db.edit_account_isAdmin(user_id, 0) # Забираем админку
        await message.answer('У тебя уже есть админка! Ну хорошо, я ее с тебя снимаю')
        return
    
    db.edit_account_isAdmin(user_id, 1) # Даем админку
    await message.answer('Поздравляю! У тебя теперь есть админка!')
