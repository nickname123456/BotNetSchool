from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging


bp = Blueprint('keyboard_schedule')# Объявляем команду




@bp.on.message(payload={'cmd': 'keyboard_schedule'})
async def keyboard_schedule(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_schedule')
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('Понедельник', {"cmd": "schedule_for_day"}))
        #Начать с новой строки
        .row()
        .add(Text('Вторник', {'cmd': 'schedule_for_day'}))
        .row()
        .add(Text('Среда', {'cmd': 'schedule_for_day'}))
        .row()
        .add(Text('Четверг', {'cmd': 'schedule_for_day'}))
        .row()
        .add(Text('Пятница', {'cmd': 'schedule_for_day'}))
        .row()
        .add(Text("Обновить", {'cmd': 'schedule_download'}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    
    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
    await message.answer('На какой день хочешь узнать расписание?', keyboard=keyboard)