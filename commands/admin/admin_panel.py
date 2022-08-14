from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging



bp = Blueprint('admin_panel')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=["админ", 'админка', 'flvby','admin'])
@bp.on.private_message(payload={'cmd': 'admin_panel'})
async def admpanel(message: Message):
    logging.info(f'{message.peer_id}: I get admin_panel')
    # ID юзера
    user_id = message.from_id

    # Проверка на админа
    if db.get_account_isAdmin(user_id) == 0:
        await message.answer('У тебя нет админских прав!')
        return

    # Создание клавиатуры
    keyboard = (
        Keyboard()
        .add(Text('Все пользователи', {'cmd': 'all_users_0'}))
        .row()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    admins = db.get_account_all_admins() # Все админы
    admins_id = [admin[0] for admin in admins] # IDшники админов
    admins = await bp.api.users.get(admins_id) # Инфа из ВК про админов
    admins = [f'{admin.first_name} {admin.last_name}' for admin in admins] # Пишем ФИ админов

    num_users = len(db.get_account_all()) # Кол-во пользователей
    num_admins = len(admins) # Кол-во админов
    await message.answer(f"Число пользователей: {num_users} \nЧисло админов: {num_admins} \n Имена администраторов: {admins}", keyboard=keyboard)