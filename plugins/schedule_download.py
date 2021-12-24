from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from vkbottle import CtxStorage
from vkbottle_types import BaseStateGroup


bp = Blueprint('schedule_download') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр

db = SQLighter('database.db')# Подключаемся к базе данных

ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class ScheduleData(BaseStateGroup):
    DAY = 0
    PHOTO = 1



@bp.on.private_message(lev='/Загрузить')
async def keyboard_schedule_download(message: Message):
    await bp.state_dispenser.set(message.peer_id, ScheduleData.DAY) # Говорим, что следующий шаг - выбор дня
    return "Введи день"

@bp.on.private_message(state=ScheduleData.DAY)
async def schedule_for_day(message: Message):
    ctx.set('day', message.text) # Загружаем во внутренне хранилище день недели
    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO) # Говорим, что следующий шаг - выбор фото
    return 'Введи фото'

@bp.on.private_message(state=ScheduleData.PHOTO)
async def schedule_for_day(message: Message):
    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
    day = ctx.get('day') # Берем из хранилища день
    photo = message.text # Берем из хранилища фото

    # Если день подходит по параматрам:
    if int(day) >= 0 and int(day) <= 4:
        db.edit_schedule(day, photo) # Записать на этот день это фото

    else:
        await message.answer('Ошибка! День должен быть >=0 и <= 4!')
        return

    await message.answer(f'{day} {photo}', attachment={photo})
    return 'ура победа'
