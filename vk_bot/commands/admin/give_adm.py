from database.methods.get import get_student_by_vk_id, get_students_with_admin
from database.methods.update import switch_student_admin
from settings import ADM_PASSWORD # Пароль для получения админки

from vkbottle.bot import Message, Blueprint

import logging



bp = Blueprint('give_admin')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




@bp.on.private_message(text=[ADM_PASSWORD])
async def give_admin(message: Message):
    logging.info(f'{message.peer_id}: I get give_admin')
    user_id = message.from_id  # ID юзера

    switch_student_admin(vk_id=user_id)

    if get_student_by_vk_id(user_id).isAdmin:
        await message.answer('Поздравляю! У тебя теперь есть админка!')

        for admin in get_students_with_admin():
            await bp.api.messages.send(message=f'❗Новый [id{user_id}|администратор]!', user_id=admin.vk_id, random_id=0, )

    else:
        await message.answer('У тебя уже есть админка! Ну хорошо, я ее с тебя снимаю')