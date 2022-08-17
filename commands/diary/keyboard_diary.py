from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
from PostgreSQLighter import db
from ns import get_next_week, get_back_week, get_week, get_diary
import logging
from VKRules import PayloadStarts
from settings import weekDays


bp = Blueprint('keyboard_diary')# Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts


@bp.on.private_message(PayloadStarts='{"cmd":"keyboard_diary')
async def keyboard_diary(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard diary')
    userId = message.from_id # ID юзера

    # Какая неделя? текущая, следущая или предыдущая?
    if len(message.payload) <= 24:
        period = ''
    else:
        period = message.payload[23:-2]
    
    if period == '':
        week = get_week()
    elif period+'_' == 'back_':
        week = get_back_week()
        period += '_'
    elif period+'_' == 'next_':
        week = get_next_week()
        period += '_'

    # Получаем дневник
    diary = await get_diary(
        db.get_account_login(userId),
        db.get_account_password(userId),
        week,
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId)
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"{period}diary_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    
    # Если текущая неделя, то можно перелистнуть назад и вперед
    if period == '':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary_back'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary_next'}))

    # Если предыдущая неделя, то можно перелистнуть только вперед
    elif period == 'back_':
        keyboard.add(Text('🟦', {'cmd': ''}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary'}))

    # Если следующая неделя, то можно перелистнуть только назад
    elif period == 'next_':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('🟦'))

    await message.answer(f'📅Текущая неделя: \n{week[0].day}.{week[0].month}.{week[0].year}\n &#12288;&#12288;--\n{week[1].day}.{week[1].month}.{week[1].year}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard diary')


@bp.on.chat_message(PayloadStarts='{"cmd":"keyboard_diary')
async def keyboard_diary(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard diary')
    chat_id = message.chat_id # ID чата

    # Какая неделя? текущая, следущая или предыдущая?
    if len(message.payload) <= 24:
        period = ''
    else:
        period = message.payload[23:-2]
    
    if period == '':
        week = get_week()
    elif period+'_' == 'back_':
        week = get_back_week()
        period += '_'
    elif period+'_' == 'next_':
        week = get_next_week()
        period += '_'

    # Получаем дневник
    diary = await get_diary(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        week,
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    # Перебирам дни недели и создаем кнопки
    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"{period}diary_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    
    # Если текущая неделя, то можно перелистнуть назад и вперед
    if period == '':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary_back'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary_next'}))

    # Если предыдущая неделя, то можно перелистнуть только вперед
    elif period == 'back_':
        keyboard.add(Text('🟦', {'cmd': ''}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary'}))

    # Если следующая неделя, то можно перелистнуть только назад
    elif period == 'next_':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('🟦'))

    await message.answer(f'📅Текущая неделя: \n{week[0].day}.{week[0].month}.{week[0].year}\n &#12288;&#12288;--\n{week[1].day}.{week[1].month}.{week[1].year}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard diary')