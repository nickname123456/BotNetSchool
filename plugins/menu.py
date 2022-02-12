from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint


bp = Blueprint('menu')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.message(text=["Меню"])
@bp.on.message(payload={'cmd': 'menu'})
async def menu(message: Message):
    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Войти', {'cmd': 'login'}), color=KeyboardButtonColor.POSITIVE)
        #Начать с новой строки
        .row()
        .add(Text('Дневник', {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Домашнее задание', {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Объявления', {'cmd': 'announcements'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Оценки', {'cmd': ' '}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('🔁', {'cmd': 'not_found'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Кирилл', {'cmd': 'not_found'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⚙', {'cmd': 'keyboard_settings'}), color=KeyboardButtonColor.SECONDARY)
    )

    #Ответ в чат
    await message.answer('Ты в главном меню.', keyboard=keyboard)
