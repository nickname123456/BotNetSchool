from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from vkbottle import CtxStorage
from vkbottle_types import BaseStateGroup
from datetime import datetime
from settings import admin_id


bp = Blueprint('update_homework') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр

db = SQLighter('database.db') # Подключаемся к базе данных

ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class HomeworkData(BaseStateGroup):
    lesson = 20
    check_admin = 21
    check_admin2 = 22
    homework = 23


@bp.on.message(payload={'cmd': 'keyboard_update_homework'})
async def keyboard_update_homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson) # Говорим, что следующий шаг - выбор урока
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
    ctx.set('lesson', message.text)  # Загружаем во временное хранилище город
    await bp.state_dispenser.set(message.peer_id, HomeworkData.check_admin)  # Говорим, что следующий шаг - проверка на админа
    return 'Введи дз'

@bp.on.chat_message(state=HomeworkData.lesson)
async def update_homework(message: Message):
    if 'public' in message.text:
        ctx.set('lesson', message.text[33:]) # Загружаем во временное хранилище урок
    else:
        ctx.set('lesson', message.text[30:]) # Загружаем во временное хранилище урок

    await bp.state_dispenser.set(message.peer_id, HomeworkData.check_admin) # Говорим, что следующий шаг - проверка на админа
    return 'Введи дз'



@bp.on.private_message(state=HomeworkData.check_admin)
async def check_admin(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    ctx.set('homework', message.text)# Загружаем во временное хранилище дз
    lesson = ctx.get('lesson') # Берем из временного хранилища урок

    # Если юзер - админ:
    if str(userInfo[0].id) == str(admin_id):
        await bp.state_dispenser.set(message.peer_id, HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб
        return 'Ты админ?'
    else:
        await bp.state_dispenser.set(int(admin_id), HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб админом
        keyboard = (
        Keyboard()
        .add(Text('Одобрить', {"prvt": f"yes_update_homework_{userInfo[0].id}_{message.peer_id}"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text('Отказать', {"prvt": f"no_update_homework_{userInfo[0].id}"}), color=KeyboardButtonColor.NEGATIVE)
        )
        await bp.api.messages.send(message=f'[id{userInfo[0].id}|Этот человек] хочет обновить дз по {lesson} на: \n{message.text}',user_id=admin_id, keyboard=keyboard, random_id=0)

@bp.on.chat_message(state=HomeworkData.check_admin)
async def check_admin(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    ctx.set('homework', message.text) # Загружаем во временное хранилище дз
    lesson = ctx.get('lesson') # Берем из временного хранилища урок

    # Если юзер - админ:
    if str(userInfo[0].id) == str(admin_id):
        await bp.state_dispenser.set(message.peer_id, HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб
        return 'Ты админ?'
    else:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку с юзером
        await bp.state_dispenser.set(int(admin_id), HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб админом
        keyboard = (
        Keyboard()
        .add(Text('Одобрить', {"chat": f"yes_update_homework_{userInfo[0].id}_{message.peer_id}"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text('Отказать', {"chat": f"no_update_homework_{userInfo[0].id}"}), color=KeyboardButtonColor.NEGATIVE)
        )
        await bp.api.messages.send(message=f'[id{userInfo[0].id}|Этот человек] хочет обновить дз по {lesson} на: \n{message.text}',user_id=admin_id, keyboard=keyboard, random_id=0)





@bp.on.private_message(state=HomeworkData.homework)
async def schedule_for_day(message: Message):
    keyboard = (
        Keyboard()
        .add(Text('Алгебра', {"cmd": "homework"}))
        .add(Text('Инф.', {"cmd": "homework"}))
        .add(Text('Геом.', {"cmd": "homework"}))
        .row()
        .add(Text('Рус. яз.', {"cmd": "homework"}))
        .add(Text('Англ. яз.', {"cmd": "homework"}))
        .add(Text('Литература', {"cmd": "homework"}))
        .row()
        .add(Text('Родн.Рус. яз.', {"cmd": "homework"}))
        .add(Text('Родн. лит-ра', {"cmd": "homework"}))
        .add(Text('ОБЖ', {"cmd": "homework"}))
        .row()
        .add(Text('Общество.', {"cmd": "homework"}))
        .add(Text('История', {"cmd": "homework"}))
        .add(Text('Геогр.', {"cmd": "homework"}))
        .row()
        .add(Text('Биол.', {"cmd": "homework"}))
        .add(Text('Физика', {"cmd": "homework"}))
        .add(Text('Химия', {"cmd": "homework"}))
        .row()
        .add(Text('Музыка', {"cmd": "homework"}))
        .add(Text('Физ-ра', {"cmd": "homework"}))
        .add(Text('Техн.', {"cmd": "homework"}))
        .row()
        .add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    lesson = ctx.get('lesson') # Берем из временного хранилища урок
    homework = ctx.get('homework') # Берем из временного хранилища дз

    # Если в обнове дз отказали
    if message.payload and 'no_update_homework_' in message.payload:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        user_id = message.payload[28:]
        user_id = int(user_id[:-2])


        await bp.api.messages.send(message=f'Администратор отказал вам в измение дз по {lesson} на:\n{homework}', user_id=user_id, keyboard=keyboard, random_id=0)

        await message.answer('Ты отказал человеку в изменение дз.')
        return

    # Если админ одобрил дз:
    elif message.payload and 'yes_update_homework_' in message.payload:
        user_id = int(message.payload[29:38]) 
        peer_id = message.payload[39:]
        peer_id = int(peer_id[:-2])

        await bp.state_dispenser.delete(int(admin_id)) # Удаляем цепочку
        userInfo = await bp.api.users.get(user_id) # Информация о юзере
    else:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    
    # Если дз обновляют из чата
    if message.payload and 'chat' in message.payload:
        chat_id = peer_id - 2000000000

    try:
        # Если дз обновляют из чата
        if message.payload and 'chat' in message.payload:
            db.edit_homework(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson,
            homework)

            db.edit_upd_date(
                db.get_chat_school(chat_id),
                db.get_chat_class(chat_id),
                lesson,
                str(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}')
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
        # Если обновляют не из чата
        else:
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
                str(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}')
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

    except TypeError:
        await message.answer(f'Человек не зарегистрирован!')
        if 'yes_update_homework_' in message.payload:
            await bp.api.messages.send(message=f'Ты не зарегистрирован! \nНапиши "Начать"', user_id=user_id, keyboard=keyboard, random_id=0)
        return

    except Exception as e:
        await message.answer(f'Произошла ошибка\n{e} \nСообщи админу')
        if 'yes_update_homework_' in message.payload:
           await bp.api.messages.send(message=f'Произошла ошибка\n{e} \nСообщи админу', user_id=user_id, keyboard=keyboard, random_id=0)
        return

    # Если одобрили запрос на обновлние дз
    if message.payload and 'yes_update_homework_' in message.payload:
        await bp.api.messages.send(message='Админ одобрил вашу заявку на обновление дз.', user_id=user_id, keyboard=keyboard, random_id=0)
        await bp.api.messages.send(message=f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', user_id=user_id, keyboard=keyboard, random_id=0)
    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', keyboard=keyboard)




@bp.on.chat_message(state=HomeworkData.homework)
async def schedule_for_day(message: Message):
    keyboard = (
        Keyboard()
        .add(Text('Алгебра', {"cmd": "homework"}))
        .add(Text('Инф.', {"cmd": "homework"}))
        .add(Text('Геом.', {"cmd": "homework"}))
        .row()
        .add(Text('Рус. яз.', {"cmd": "homework"}))
        .add(Text('Англ. яз.', {"cmd": "homework"}))
        .add(Text('Литература', {"cmd": "homework"}))
        .row()
        .add(Text('Родн.Рус. яз.', {"cmd": "homework"}))
        .add(Text('Родн. лит-ра', {"cmd": "homework"}))
        .add(Text('ОБЖ', {"cmd": "homework"}))
        .row()
        .add(Text('Общество.', {"cmd": "homework"}))
        .add(Text('История', {"cmd": "homework"}))
        .add(Text('Геогр.', {"cmd": "homework"}))
        .row()
        .add(Text('Биол.', {"cmd": "homework"}))
        .add(Text('Физика', {"cmd": "homework"}))
        .add(Text('Химия', {"cmd": "homework"}))
        .row()
        .add(Text('Музыка', {"cmd": "homework"}))
        .add(Text('Физ-ра', {"cmd": "homework"}))
        .add(Text('Техн.', {"cmd": "homework"}))
        .row()
        .add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    lesson = ctx.get('lesson') # Берем из временного хранилища урок
    homework = ctx.get('homework') # Берем из временного хранилища дз

    # Если в обнове дз отказали
    if message.payload and 'no_update_homework_' in message.payload:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        user_id = message.payload[28:]
        user_id = int(user_id[:-2])

        #try:
        await bp.api.messages.send(message=f'Администратор отказал вам в измение дз по {lesson} на:\n{homework}', user_id=user_id, keyboard=keyboard, random_id=0)
        #except VKAPIError[901] as e:
        #    await message.answer("не могу отправить сообщение из-за настроек приватности")

        await message.answer('Ты отказал человеку в изменение дз.')
        return

    peer_id = message.peer_id
    chat_id = message.chat_id

    await bp.state_dispenser.delete(peer_id) # Удаляем цепочку

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
            str(f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}')
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
    except Exception as e:
       await message.answer(f'Произошла ошибка\n{e} Сообщи админу')
       

    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', keyboard=keyboard)