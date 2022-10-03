from database.methods.get import get_all_students, get_student_by_vk_id, get_students_with_admin

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('admin_panel')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=["админ", 'админка', 'flvby','admin',
                            "/админ", '/админка', '/flvby','/admin'])
@bp.on.private_message(payload={'cmd': 'admin_panel'})
async def admpanel(message: Message):
    logging.info(f'{message.peer_id}: I get admin_panel')
    # ID юзера
    user_id = message.from_id
    student = get_student_by_vk_id(user_id)

    # Проверка на админа
    if not student.isAdmin:
        await message.answer('У тебя нет админских прав!')
        return

    # Создание клавиатуры
    keyboard = (
        Keyboard()
        .add(Text('Все пользователи', {'cmd': 'all_users_0'}))
        .row()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    admins = get_students_with_admin() # Все админы
    admins_id = [admin.vk_id for admin in admins] # IDшники админов
    admins = await bp.api.users.get(admins_id) # Инфа из ВК про админов
    admins = [f'{admin.first_name} {admin.last_name}' for admin in admins] # Пишем ФИ админов

    num_users = len(get_all_students()) # Кол-во пользователей
    num_admins = len(admins) # Кол-во админов
    await message.answer(f"Число пользователей: {num_users} \nЧисло админов: {num_admins} \n Имена администраторов: {admins}", keyboard=keyboard)