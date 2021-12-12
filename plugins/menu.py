from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint


bp = Blueprint('menu')
bp.on.vbml_ignore_case = True




#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.message(text=["Меню"])
@bp.on.message(payload={'cmd': 'menu'})
async def menu(message: Message):
    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Войти', {'cmd': 'login'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('Дневник', {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Домашнее задание', {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Объявления', {'cmd': 'announcements'}), color=KeyboardButtonColor.PRIMARY)
    )

    #Ответ в чат
    await message.answer('Ты в главном меню.', keyboard=keyboard)
