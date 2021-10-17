from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint


bp = Blueprint('keyboard_diary')

@bp.on.message(payload={'cmd': 'keyboard_diary'})
async def keyboard_diary(message: Message):

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
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('На какой день хочешь узнать расписание?', keyboard=keyboard)
