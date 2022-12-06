from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('keyboard_schedule')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр



@bp.on.message(text=['расписание', '/расписание', '/hfcgbcfybt', '/расп', '/hfcg', '/rasp', 'скиньте расписание', 'дайте расписание'])
@bp.on.message(payload={'cmd': 'keyboard_schedule'})
async def keyboard_schedule(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_schedule')
    if (await bp.state_dispenser.get(message.peer_id)): 
        if message.from_id == (await bp.state_dispenser.get(message.peer_id)).peer_id:
            await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку состояний
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
        .add(Text('Суббота', {'cmd': 'schedule_for_day'}))
        .row()
        .add(Text("Обновить", {'cmd': 'schedule_download'}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    
    logging.info(f'{message.peer_id}: I sent keyboard_schedule')
    await message.answer('🤔На какой день хотите узнать расписание?', keyboard=keyboard)