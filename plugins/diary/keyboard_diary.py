from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_next_period, get_back_period, get_period
import logging


bp = Blueprint('keyboard_diary')# Объявляем команду
db = SQLighter('database.db') # Подключаемся к базе данных


@bp.on.message(payload={'cmd': 'keyboard_diary'})
async def keyboard_diary(message: Message):
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере
    logging.info(f'{message.peer_id}: I get keyboard diary')

    db.edit_account_week(userInfo[0].id, 0)# Редактируем неделю, на которой юзер

    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('Понедельник', {"cmd": "diary_for_day"}))
        #Начать с новой строки
        .row()
        .add(Text('Вторник', {'cmd': 'diary_for_day'}))
        .row()
        .add(Text('Среда', {'cmd': 'diary_for_day'}))
        .row()
        .add(Text('Четверг', {'cmd': 'diary_for_day'}))
        .row()
        .add(Text('Пятница', {'cmd': 'diary_for_day'}))
        .row()
        .add(Text('◀', {'cmd': 'keyboard_diary_back'}))
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        .add(Text('▶', {'cmd': 'keyboard_diary_next'}))
    )

    await message.answer(f'Текущая неделя: \n{get_period()[0]}\n-\n{get_period()[1]} \nНа какой день хочешь узнать расписание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send keyboard diary')




@bp.on.message(payload={'cmd': 'keyboard_diary_back'})
async def keyboard_diary(message: Message):
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере
    logging.info(f'{message.peer_id}: I get keyboard diary')

    db.edit_account_week(userInfo[0].id, -1)# Редактируем неделю, на которой юзер

    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('Понедельник', {"cmd": "back_diary_for_day"}))
        #Начать с новой строки
        .row()
        .add(Text('Вторник', {'cmd': 'back_diary_for_day'}))
        .row()
        .add(Text('Среда', {'cmd': 'back_diary_for_day'}))
        .row()
        .add(Text('Четверг', {'cmd': 'back_diary_for_day'}))
        .row()
        .add(Text('Пятница', {'cmd': 'back_diary_for_day'}))
        .row()
        .add(Text('🟦', {'cmd': ''}))
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        .add(Text('▶', {'cmd': 'keyboard_diary'}))
    )

    await message.answer(f'Текущая неделя: \n{get_back_period()[0]}\n-\n{get_back_period()[1]} \nНа какой день хочешь узнать расписание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send back keyboard diary')



@bp.on.message(payload={'cmd': 'keyboard_diary_next'})
async def keyboard_diary(message: Message):
    userInfo = await bp.api.users.get(message.from_id)# Информация о юзере
    logging.info(f'{message.peer_id}: I get keyboard diary')

    db.edit_account_week(userInfo[0].id, 1)# Редактируем неделю, на которой юзер

    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('Понедельник', {"cmd": "next_diary_for_day"}))
        #Начать с новой строки
        .row()
        .add(Text('Вторник', {'cmd': 'next_diary_for_day'}))
        .row()
        .add(Text('Среда', {'cmd': 'next_diary_for_day'}))
        .row()
        .add(Text('Четверг', {'cmd': 'next_diary_for_day'}))
        .row()
        .add(Text('Пятница', {'cmd': 'next_diary_for_day'}))
        .row()
        .add(Text('◀', {'cmd': 'keyboard_diary'}))
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
        .add(Text('🟦'))
    )

    await message.answer(f'Текущая неделя: \n{get_next_period()[0]}\n-\n{get_next_period()[1]} \nНа какой день хочешь узнать расписание?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send next keyboard diary')