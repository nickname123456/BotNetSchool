from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from ns import getSettings
import logging



bp = Blueprint('information')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр



@bp.on.private_message(payload={'cmd': 'information'})
async def private_information(message: Message):
    logging.info(f'{message.peer_id}: I get information')
    user_id = message.from_id # ID юзера

    try:
        result= await getSettings( # Получаем приватные данные из СГО
            db.get_account_login(user_id),
            db.get_account_password(user_id),
            db.get_account_school(user_id),
            db.get_account_link(user_id),
            db.get_account_studentId(user_id),
            db.get_account_class(user_id)
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    await message.answer(result)
    logging.info(f'{message.peer_id}: I sent information')


@bp.on.chat_message(payload={'cmd': 'information'})
async def chat_information(message: Message):
    logging.info(f'{message.peer_id}: I get information')
    # Айди чата:
    chat_id = message.chat_id

    try:
        result= await getSettings( # Получаем приватные данные СГО
            db.get_chat_login(chat_id),
            db.get_chat_password(chat_id),
            db.get_chat_school(chat_id),
            db.get_chat_link(chat_id),
            db.get_chat_studentId(chat_id),
            db.get_chat_class(chat_id)
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    await message.answer(result)
    logging.info(f'{message.peer_id}: I sent information')