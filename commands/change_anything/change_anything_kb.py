from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
import logging


bp = Blueprint('change_anything_kb')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.message(payload={'cmd': 'change_anything_kb'})
async def change_anything_kb(message: Message):
    logging.info(f'{message.peer_id}: I get change_anything_kb')

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        .add(Text('Сменить ребенка', {'cmd': 'change_student'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Сменить аккаунт', {'cmd': 'start'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    #Ответ в чат
    await message.answer('🔄Что ты хочешь поменять?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent change_anything_kb')