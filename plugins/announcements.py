from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_announcements
from settings import admin_login, admin_password, admin_link, admin_school


bp = Blueprint('announcements')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')


@bp.on.private_message(text=["Объявления <amount>", "Объявления"])
@bp.on.private_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    userInfo = await bp.api.users.get(message.from_id)

    announcements = await get_announcements(db.get_account_login(userInfo[0].id),
                                  db.get_account_password(userInfo[0].id),
                                  amount,
                                  db.get_account_school(userInfo[0].id),
                                  db.get_account_link(userInfo[0].id))

    for i in announcements:
        await message.answer(i)



@bp.on.chat_message(text=["Объявления <amount>", "Объявления"])
@bp.on.chat_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    chat_id = message.chat_id
    print(chat_id)

    try:
        announcements = await get_announcements(
                                    db.get_chat_login(chat_id),
                                    db.get_chat_password(chat_id),
                                    amount,
                                    db.get_chat_school(chat_id),
                                    db.get_chat_link(chat_id))
    except:
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return

    for i in announcements:
        await message.answer(i)
