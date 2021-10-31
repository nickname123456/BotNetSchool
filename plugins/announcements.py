from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_announcements


bp = Blueprint('announcements')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')


@bp.on.message(text=["Объявления <amount>", "Объявления"])
@bp.on.message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    userInfo = await bp.api.users.get(message.from_id)

    announcements = await get_announcements(db.get_account_login(userInfo[0].id),
                                  db.get_account_password(userInfo[0].id),
                                  amount,
                                  db.get_account_school(userInfo[0].id),
                                  db.get_account_link(userInfo[0].id))

    for i in announcements:
        await message.answer(i)
