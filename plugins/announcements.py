from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_announcements


bp = Blueprint('announcements')
db = SQLighter('database.db')


@bp.on.message(text=["Объявления <amount>", "Объявления"])
@bp.on.message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    userInfo = await bp.api.users.get(message.from_id)

    announcements = await get_announcements(db.get_account_login(userInfo[0].id),
                                  db.get_account_password(userInfo[0].id),
                                  amount)

    for i in announcements:
        await message.answer(i)
