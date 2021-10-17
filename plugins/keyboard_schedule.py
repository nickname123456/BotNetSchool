from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint


bp = Blueprint('keyboard_schedule')



@bp.on.message(payload={'cmd': 'keyboard_schedule'})
async def keyboard_schedule(message: Message):
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
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('На какой день хочешь узнать расписание?', keyboard=keyboard)
