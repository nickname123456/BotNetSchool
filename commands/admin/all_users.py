from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts



bp = Blueprint('all_users')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"all_users_')
async def all_users(message: Message, userId=None):
    logging.info(f'{message.peer_id}: I get all_users')
    user_id = message.from_id # ID юзера

    # Проверка на админа
    if db.get_account_isAdmin(user_id) == 0:
        await message.answer('У тебя нет админских прав!')
        return

    users = db.get_account_all()  # Все пользователи
    # Делим всех юзеров на ровные части, для того, чтобы их всех можно было уместить в клавиатуры
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

    # Делаем Клавиатуру с ФИ всех юзеров
    keyboard = Keyboard()
    for i in users_id[int(message.payload[18:-2])]:
        user = await bp.api.users.get(i) # Инфа мз ВК
        user = user[0] # Берем 1ого юзера
        user = f'{user.first_name} {user.last_name}' # Берем ФИ
        keyboard.add(Text(user, {'cmd': f'view_{i}'})) # Вставляем в кнопку ФИ и в колбэк ID
        keyboard.row()
    

    page = int(message.payload[18:-2]) # Страница, которую сейчас смотрит админ
    
    # Можно ли перелистнуть стр с юзерами назад
    if page <= 1:
        keyboard.add(Text('🟦'))
    else:
        keyboard.add(Text('◀', {'cmd': f'all_users_{page-1}'}))

    keyboard.add(Text('Назад', {'cmd': 'admin_panel'}), color=KeyboardButtonColor.NEGATIVE)

    # Можно ли прелестнуть стр с юзерами вперед
    if page >= max(users_id):
        keyboard.add(Text('🟦'))
    else:
        keyboard.add(Text('▶', {'cmd': f'all_users_{page+1}'}))


    await message.answer('Выбирай', keyboard=keyboard)