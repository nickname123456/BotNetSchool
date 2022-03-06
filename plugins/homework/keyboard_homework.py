from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
import logging


bp = Blueprint('keyboard_homework')# Объявляем команду




@bp.on.message(payload={'cmd': 'keyboard_homework'})
async def keyboard_schedule(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_homework')
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('Алгебра', {"cmd": "homework"}))
        .add(Text('Инф.', {"cmd": "homework"}))
        .add(Text('Геом.', {"cmd": "homework"}))
        #Начать с новой строки
        .row()
        .add(Text('Рус. яз.', {"cmd": "homework"}))
        .add(Text('Англ. яз.', {"cmd": "homework"}))
        .add(Text('Литература', {"cmd": "homework"}))
        .row()
        .add(Text('Родн.Рус. яз.', {"cmd": "homework"}))
        .add(Text('Родн. лит-ра', {"cmd": "homework"}))
        .add(Text('ОБЖ', {"cmd": "homework"}))
        .row()
        .add(Text('Общество.', {"cmd": "homework"}))
        .add(Text('История', {"cmd": "homework"}))
        .add(Text('Геогр.', {"cmd": "homework"}))
        .row()
        .add(Text('Биол.', {"cmd": "homework"}))
        .add(Text('Физика', {"cmd": "homework"}))
        .add(Text('Химия', {"cmd": "homework"}))
        .row()
        .add(Text('Музыка', {"cmd": "homework"}))
        .add(Text('Физ-ра', {"cmd": "homework"}))
        .add(Text('Техн.', {"cmd": "homework"}))
        .row()
        .add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('На какой урок хочешь узнать домашнее задание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard_homework')