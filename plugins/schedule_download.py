from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_diary
import netschoolapi
from vkbottle import CtxStorage
from vkbottle_types import BaseStateGroup


bp = Blueprint('schedule_download')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')

ctx = CtxStorage()

class ScheduleData(BaseStateGroup):
    DAY = 0
    PHOTO = 1



@bp.on.message(lev='/Загрузить')
async def keyboard_schedule_download(message: Message):
    await bp.state_dispenser.set(message.peer_id, ScheduleData.DAY)
    return "Введи день"

@bp.on.message(state=ScheduleData.DAY)
async def schedule_for_day(message: Message):
    ctx.set('day', message.text)
    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO)
    return 'Введи фото'

@bp.on.message(state=ScheduleData.PHOTO)
async def schedule_for_day(message: Message):
    await bp.state_dispenser.delete(message.peer_id)
    day = ctx.get('day')
    photo = message.text

    if '0' == day:
        db.edit_schedule(0, photo)
    elif '1' == day:
        db.edit_schedule(1, photo)
    elif '2' == day:
        db.edit_schedule(2, photo)
    elif '3' == day:
        db.edit_schedule(3, photo)
    elif '4' == day:
        db.edit_schedule(4, photo)

    await message.answer(f'{day} {photo}', attachment={photo})
    return 'ура победа'
