from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging



bp = Blueprint('admin_panel')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=["админ", 'админка', 'flvby','admin'])
@bp.on.private_message(payload={'cmd': 'admin_panel'})
async def admpanel(message: Message, userId=None):
    logging.info(f'{message.peer_id}: I get admin_panel')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if db.get_account_isAdmin(user_id) == 0:
        await message.answer('У тебя нет админских прав!')
        return
    
    keyboard = (
        Keyboard()
        .add(Text('Все пользователи', {'cmd': 'all_users_0'}))
        .row()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    admins = [user for user in db.get_account_all() if user[20] == 1]
    admins_id = [admin[0] for admin in admins]
    admins = await bp.api.users.get(admins_id)
    admins = [f'{admin.first_name} {admin.last_name}' for admin in admins]

    num_users = len(db.get_account_all())
    num_admins = len(admins)
    await message.answer(f"Число пользователей: {num_users} \nЧисло админов: {num_admins} \n Имена администраторов: {admins}", keyboard=keyboard)