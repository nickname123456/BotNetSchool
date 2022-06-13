from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
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
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере
    userId = userInfo[0].id

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

    diary = await get_diary(
        db.get_account_login(userId),
        db.get_account_password(userId),
        week,
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId)
    )

    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"{period}diary_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    
    if period == '':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary_back'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary_next'}))

    elif period == 'back_':
        keyboard.add(Text('🟦', {'cmd': ''}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary'}))

    elif period == 'next_':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('🟦'))

    await message.answer(f'Текущая неделя: \n{week[0]}\n-\n{week[1]} \nНа какой день хочешь узнать расписание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard diary')


@bp.on.chat_message(PayloadStarts='{"cmd":"keyboard_diary')
async def keyboard_diary(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard diary')
    chat_id = message.chat_id

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

    diary = await get_diary(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        week,
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    keyboard = Keyboard()
    day_number = 0
    for day in diary['weekDays']:
        for i in weekDays:
            if int(str(day['date'])[8:-9]) - int(str(week[0])[8:]) == i:
                keyboard.add(Text(weekDays[i], {"cmd": f"{period}diary_for_day_{day_number}"}))
                keyboard.row()
        day_number += 1
    
    if period == '':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary_back'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary_next'}))

    elif period == 'back_':
        keyboard.add(Text('🟦', {'cmd': ''}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('▶', {'cmd': 'keyboard_diary'}))

    elif period == 'next_':
        keyboard.add(Text('◀', {'cmd': 'keyboard_diary'}))
        keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.add(Text('🟦'))

    await message.answer(f'Текущая неделя: \n{week[0]}\n-\n{week[1]} \nНа какой день хочешь узнать расписание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard diary')