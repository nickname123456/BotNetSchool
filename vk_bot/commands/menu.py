from database.methods.get import get_student_by_vk_id, get_chat_by_vk_id
from netschoolapi import NetSchoolAPI

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('menu')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.private_message(text=["Меню", '/menu', '/vty.', '/меню'])
@bp.on.private_message(payload={'cmd': 'menu'})
async def private_menu(message: Message):
    logging.info(f'{message.peer_id}: I get menu')
    user_id = message.from_id

    student = get_student_by_vk_id(user_id)
    try:
        api = NetSchoolAPI(student.link) # Логинимся в СГО
        await api.login(
            student.login, 
            student.password, 
            student.school,
            student.studentId
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    settings = await api.userInfo()
    await api.logout()
    name = settings['Имя']

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
        .add(Text('Отчеты', {'cmd': 'reports'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('🔁', {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'{name}', {'cmd': 'information'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⚙', {'cmd': 'keyboard_settings'}), color=KeyboardButtonColor.SECONDARY)
    )

    #Ответ в чат
    await message.answer('Вы в главном меню.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent menu')




#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.chat_message(text=["Меню", '/menu', '/vty.', '/меню'])
@bp.on.chat_message(payload={'cmd': 'menu'})
async def chat_menu(message: Message):
    logging.info(f'{message.peer_id}: I get menu')
    # Айди чата:
    chat_id = message.chat_id

    chat = get_chat_by_vk_id(chat_id)
    try:
        api = NetSchoolAPI(chat.link) # Логинимся в СГО
        await api.login(
            chat.login, 
            chat.password, 
            chat.school,
            chat.studentId
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!\n 🤔Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    settings = await api.userInfo()
    await api.logout()
    name = settings['Имя']

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
        .add(Text('Отчеты', {'cmd': 'reports'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('🔁', {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'{name}', {'cmd': 'information'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⚙', {'cmd': 'keyboard_settings'}), color=KeyboardButtonColor.SECONDARY)
    )

    #Ответ в чат
    await message.answer('Вы в главном меню.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent menu')