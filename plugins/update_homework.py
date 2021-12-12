from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_diary
import netschoolapi
from vkbottle import CtxStorage
from vkbottle_types import BaseStateGroup
from datetime import datetime


bp = Blueprint('update_homework')
bp.on.vbml_ignore_case = True

db = SQLighter('database.db')

ctx = CtxStorage()

class HomeworkData(BaseStateGroup):
    lesson = 20
    homework = 21


@bp.on.message(payload={'cmd': 'keyboard_update_homework'})
async def keyboard_update_homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson)
    keyboard = (
        Keyboard()
        .add(Text('Алгебра', {"cmd": "update_homework"}))
        .add(Text('Инф.', {"cmd": "update_homework"}))
        .add(Text('Геом.', {"cmd": "update_homework"}))
        .row()
        .add(Text('Рус. яз.', {"cmd": "update_homework"}))
        .add(Text('Англ. яз.', {"cmd": "update_homework"}))
        .add(Text('Литература', {"cmd": "update_homework"}))
        .row()
        .add(Text('Родн.Рус. яз.', {"cmd": "update_homework"}))
        .add(Text('Родн. лит-ра', {"cmd": "update_homework"}))
        .add(Text('ОБЖ', {"cmd": "update_homework"}))
        .row()
        .add(Text('Общество.', {"cmd": "update_homework"}))
        .add(Text('История', {"cmd": "update_homework"}))
        .add(Text('Геогр.', {"cmd": "update_homework"}))
        .row()
        .add(Text('Биол.', {"cmd": "update_homework"}))
        .add(Text('Физика', {"cmd": "update_homework"}))
        .add(Text('Химия', {"cmd": "update_homework"}))
        .row()
        .add(Text('Музыка', {"cmd": "update_homework"}))
        .add(Text('Физ-ра', {"cmd": "update_homework"}))
        .add(Text('Техн.', {"cmd": "update_homework"}))
        .row()
        .add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('На какой урок хочешь изменить дз?', keyboard=keyboard)




@bp.on.private_message(state=HomeworkData.lesson)
async def update_homework(message: Message):
    ctx.set('lesson', message.text)
    await bp.state_dispenser.set(message.peer_id, HomeworkData.homework)
    return 'Введи дз'

@bp.on.chat_message(state=HomeworkData.lesson)
async def update_homework(message: Message):
    ctx.set('lesson', message.text[33:])
    await bp.state_dispenser.set(message.peer_id, HomeworkData.homework)
    return 'Введи дз'



@bp.on.private_message(state=HomeworkData.homework)
async def schedule_for_day(message: Message):
    await bp.state_dispenser.delete(message.peer_id)
    userInfo = await bp.api.users.get(message.from_id)
    lesson = ctx.get('lesson')
    homework = message.text

    try:
        db.edit_homework(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            lesson,
            homework
        )

        db.edit_upd_date(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            lesson,
            str(datetime.now())
        )

        await message.answer('Ты успешно обновил дз')

        homework = db.get_homework(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            lesson
        )

        upd_date = db.get_upd_date(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            lesson
        )
    except:
        message.answer('Произошла ошибка! Сообщи админу')

    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}')



@bp.on.chat_message(state=HomeworkData.homework)
async def schedule_for_day(message: Message):
    await bp.state_dispenser.delete(message.peer_id)
    chat_id = message.chat_id
    lesson = ctx.get('lesson')
    homework = message.text

    try:
        db.edit_homework(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson,
            homework
        )

        db.edit_upd_date(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson,
            str(datetime.now())
        )

        await message.answer('Ты успешно обновил дз')

        homework = db.get_homework(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson
        )

        upd_date = db.get_upd_date(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson
        )
    except:
        message.answer('Произошла ошибка! Сообщи админу')

    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}')