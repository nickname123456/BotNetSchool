from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts



bp = Blueprint('all_users')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"all_users_')
async def all_users(message: Message, userId=None):
    logging.info(f'{message.peer_id}: I get all_users')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if db.get_account_isAdmin(user_id) == 0:
        await message.answer('У тебя нет админских прав!')
        return
    

    users = db.get_account_all()
    users_id = {0:[]}
    counter = 0
    list_counter = 0
    for i in users:
        if counter == 5:
            counter = 0
            list_counter += 1
            users_id[list_counter] = []

        users_id[list_counter].append(i[0])
        counter += 1

    
    keyboard = Keyboard()
    for i in users_id[int(message.payload[18:-2])]:
        user = await bp.api.users.get(i)
        user = user[0]
        user = f'{user.first_name} {user.last_name}'
        keyboard.add(Text(user, {'cmd': f'view_{i}'}))
        keyboard.row()
    


    if int(message.payload[18:-2]) <= 1:
        keyboard.add(Text('🟦', {'cmd': 'admin_panel'}))
    else:
        keyboard.add(Text('◀', {'cmd': 'admin_panel'}))

    keyboard.add(Text('Назад', {'cmd': 'admin_panel'}), color=KeyboardButtonColor.NEGATIVE)

    if int(message.payload[18:-2]) >= max(users_id):
        keyboard.add(Text('🟦', {'cmd': 'admin_panel'}))
    else:
        keyboard.add(Text('▶', {'cmd': 'admin_panel'}))


    await message.answer('Выбирай', keyboard=keyboard)