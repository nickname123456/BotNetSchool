from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from vkbottle import Keyboard, KeyboardButtonColor, Text


bp = Blueprint('correction_mark_choice_mark') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений

db = SQLighter('database.db')# Подключаемся к базеданных


@bp.on.private_message(payload={'cmd': 'correction_mark_choice_mark'})
async def private_correction_mark_choice_mark(message: Message):
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if str(message.text) == 'Алгебра':
        lesson = 'Алгебра'
    elif str(message.text) == 'Инф.':
        lesson = 'Информатика'
    elif str(message.text) == 'Геом.':
        lesson = 'Геометрия'
    elif str(message.text) == 'Рус. яз.':
        lesson = 'Русский язык'
    elif str(message.text) == 'Англ. яз.':
        lesson = 'Иностранный язык (англ.язык)'
    elif str(message.text) == 'Литература':
        lesson = 'Литература.'
    elif str(message.text) == 'Родн.Рус. яз.':
        lesson = 'Родной русский язык 5-11'
    elif str(message.text) == 'Родн. лит-ра':
        lesson = 'Родная (русская) литература 5-9'
    elif str(message.text) == 'ОБЖ':
        lesson = 'Основы безопасности жизнедеятельности'
    elif str(message.text) == 'Общество.':
        lesson = 'Обществознание'
    elif str(message.text) == 'История':
        lesson = 'История'
    elif str(message.text) == 'Геогр.':
        lesson = 'География'
    elif str(message.text) == 'Биол.':
        lesson = 'Биология'
    elif str(message.text) == 'Физика':
        lesson = 'Физика'
    elif str(message.text) == 'Химия':
        lesson = 'Химия'
    elif str(message.text) == 'Физ-ра':
        lesson = 'Физическая культура'
    elif str(message.text) == 'Музыка':
        lesson = 'Музыка'
    elif str(message.text) == 'Техн.':
        lesson = 'Технология'

    db.edit_account_correction_lesson(user_id, lesson)

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('5️⃣', {"cmd": "correction_mark"}))
        .add(Text('4️⃣', {"cmd": "correction_mark"}))
        .add(Text('3️⃣', {"cmd": "correction_mark"}))
        .row()
        .add(Text("Назад", {'cmd': 'marks'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('Какую оценку хочешь?', keyboard=keyboard)











@bp.on.chat_message(payload={'cmd': 'correction_mark_choice_mark'})
async def chat_correction_mark_choice_mark(message: Message):
    # Айди чата:
    chat_id = message.chat_id
    
    if str(message.text) == 'Алгебра':
        lesson = 'Алгебра'
    elif str(message.text) == 'Инф.':
        lesson = 'Информатика'
    elif str(message.text) == 'Геом.':
        lesson = 'Геометрия'
    elif str(message.text) == 'Рус. яз.':
        lesson = 'Русский язык'
    elif str(message.text) == 'Англ. яз.':
        lesson = 'Иностранный язык (англ.язык)'
    elif str(message.text) == 'Литература':
        lesson = 'Литература.'
    elif str(message.text) == 'Родн.Рус. яз.':
        lesson = 'Родной русский язык 5-11'
    elif str(message.text) == 'Родн. лит-ра':
        lesson = 'Родная (русская) литература 5-9'
    elif str(message.text) == 'ОБЖ':
        lesson = 'Основы безопасности жизнедеятельности'
    elif str(message.text) == 'Общество.':
        lesson = 'Обществознание'
    elif str(message.text) == 'История':
        lesson = 'История'
    elif str(message.text) == 'Геогр.':
        lesson = 'География'
    elif str(message.text) == 'Биол.':
        lesson = 'Биология'
    elif str(message.text) == 'Физика':
        lesson = 'Физика'
    elif str(message.text) == 'Химия':
        lesson = 'Химия'
    elif str(message.text) == 'Физ-ра':
        lesson = 'Физическая культура'
    elif str(message.text) == 'Музыка':
        lesson = 'Музыка'
    elif str(message.text) == 'Техн.':
        lesson = 'Технология'

    db.edit_chat_correction_lesson(chat_id, lesson)

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('5️⃣', {"cmd": "correction_mark"}))
        .add(Text('4️⃣', {"cmd": "correction_mark"}))
        .add(Text('3️⃣', {"cmd": "correction_mark"}))
        .row()
        .add(Text("Назад", {'cmd': 'correction_mark_choice_lesson'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('Какую оценку хочешь?', keyboard=keyboard)
