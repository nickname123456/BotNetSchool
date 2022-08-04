from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD 
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
from datetime import datetime
from settings import admin_id
import logging
import asyncio


bp = Blueprint('update_homework') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр


ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class HomeworkData(BaseStateGroup):
    lesson = 20
    check_admin = 21
    homework = 22


@bp.on.private_message(payload={'cmd': 'keyboard_update_homework'})
async def private_keyboard_update_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_update_homework')
    userInfo = await bp.api.users.get(message.from_id)
    userId = userInfo[0].id

    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson) # Говорим, что следующий шаг - выбор урока

    keyboard = Keyboard()

    lessons = db.get_lessons_with_homework(
        db.get_account_school(userId),
        db.get_account_class(userId)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "update_homework"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('На какой урок хочешь изменить дз? Если для нужного предмета нет кнопки, то просто напиши название.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send list of lessons')


@bp.on.chat_message(payload={'cmd': 'keyboard_update_homework'})
async def chat_keyboard_update_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_update_homework')
    chat_id = message.chat_id

    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson) # Говорим, что следующий шаг - выбор урока

    keyboard = Keyboard()

    lessons = db.get_lessons_with_homework(
        db.get_chat_school(chat_id),
        db.get_chat_class(chat_id)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "update_homework"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('На какой урок хочешь изменить дз? Если для нужного предмета нет кнопки, то просто напиши название.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send list of lessons')




@bp.on.message(state=HomeworkData.lesson)
async def get_new_homework(message: Message):
    logging.info(f'{message.peer_id}: I get lesson in update_homework')
    userInfo = await bp.api.users.get(message.from_id)
    ctx.set('lesson', message.text) # Загружаем во временное хранилище урок

    if str(userInfo[0].id) == str(admin_id): await bp.state_dispenser.set(message.peer_id, HomeworkData.homework)
    else: await bp.state_dispenser.set(message.peer_id, HomeworkData.check_admin) # Говорим, что следующий шаг - проверка на админа
    
    logging.info(f'{message.peer_id}: I sent a question about homework')
    return 'Введи дз'



@bp.on.private_message(state=HomeworkData.check_admin)
async def private_check_admin(message: Message):
    logging.info(f'{message.peer_id}: I get homework in update_homework')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    ctx.set('homework', message.text)# Загружаем во временное хранилище дз
    lesson = ctx.get('lesson') # Берем из временного хранилища урок

    await bp.state_dispenser.set(int(admin_id), HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб админом
    keyboard = (
    Keyboard()
    .add(Text('Одобрить', {"prvt": f"yes_update_homework_{userInfo[0].id}_{message.peer_id}"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text('Отказать', {"prvt": f"no_update_homework_{userInfo[0].id}"}), color=KeyboardButtonColor.NEGATIVE)
    )
    logging.info(f'{message.peer_id}: I sent a question about approval')
    await bp.api.messages.send(message=f'[id{userInfo[0].id}|Этот человек] хочет обновить дз по {lesson} на: \n{message.text}',user_id=admin_id, keyboard=keyboard, random_id=0)
    await message.answer('Я отправил это домашнее задание администратору. Я сообщу, если он его одобрит.')

@bp.on.chat_message(state=HomeworkData.check_admin)
async def chat_check_admin(message: Message):
    logging.info(f'{message.peer_id}: I get homework in update_homework')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    ctx.set('homework', message.text) # Загружаем во временное хранилище дз
    lesson = ctx.get('lesson') # Берем из временного хранилища урок

    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку с юзером
    await bp.state_dispenser.set(int(admin_id), HomeworkData.homework) # Говорим, что следующий шаг - залив дз в дб админом
    keyboard = (
    Keyboard()
    .add(Text('Одобрить', {"chat": f"yes_update_homework_{userInfo[0].id}_{message.peer_id}"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text('Отказать', {"chat": f"no_update_homework_{userInfo[0].id}"}), color=KeyboardButtonColor.NEGATIVE)
    )
    logging.info(f'{message.peer_id}: I sent a question about approval')
    await bp.api.messages.send(message=f'[id{userInfo[0].id}|Этот человек] хочет обновить дз по {lesson} на: \n{message.text}',user_id=admin_id, keyboard=keyboard, random_id=0)
    return 'Я отправил это домашнее задание администратору. Я сообщу, если он его одобрит.'




@bp.on.private_message(state=HomeworkData.homework)
async def private_edit_hamework(message: Message):
    logging.info(f'{message.peer_id}: Im at the end of update_homework')
    userInfo = await bp.api.users.get(message.from_id)
    userId = userInfo[0].id

    if message.payload is None: # если человек попал в этот стейт прямиком из указания дз (у админа не спрашивалось разрешение)
        ctx.set('homework', message.text)# Загружаем во временное хранилище дз
    
    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = db.get_lessons_with_homework(
        db.get_account_school(userId),
        db.get_account_class(userId)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "homework"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    lesson = ctx.get('lesson') # Берем из временного хранилища урок
    homework = ctx.get('homework') # Берем из временного хранилища дз

    # Если в обнове дз отказали
    if message.payload and 'no_update_homework_' in message.payload:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        user_id = int(message.payload[28:-2])

        await bp.api.messages.send(message=f'Администратор отказал вам в измение дз по {lesson} на:\n{homework}', user_id=user_id, keyboard=keyboard, random_id=0)
        logging.info(f'{message.peer_id}: I sent a refusal')

        await message.answer('Ты отказал человеку в изменение дз.', keyboard=EMPTY_KEYBOARD)
        return

    # Если админ одобрил дз:
    elif message.payload and 'yes_update_homework_' in message.payload:
        user_id = int(message.payload[29:38]) 
        peer_id = int(message.payload[39:-2])

        await bp.state_dispenser.delete(int(admin_id)) # Удаляем цепочку
        userInfo = await bp.api.users.get(user_id) # Информация о юзере
    else:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    
    # Если дз обновляют из чата
    if message.payload and 'chat' in message.payload:
        chat_id = peer_id - 2000000000

    upd_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}'
    
    try:
        # Если дз обновляют из чата
        if message.payload and 'chat' in message.payload:
            clas = db.get_chat_class(chat_id)
            school = db.get_chat_school(chat_id)

            if (lesson,) in lessons:
                db.edit_homework(
                    school,
                    clas,
                    lesson,
                    homework
                )
                db.edit_upd_date(
                    school,
                    clas,
                    lesson,
                    upd_date
                )
            else:
                db.add_lesson_with_homework(lesson, school, clas, homework, upd_date)
            db.commit()

            await message.answer('Ты успешно обновил дз', keyboard=keyboard)
            logging.info(f'{message.peer_id}: I sent a success')

        # Если обновляют не из чата
        else:
            school = db.get_account_school(userInfo[0].id)
            clas = db.get_account_class(userInfo[0].id)

            if (lesson,) in lessons:
                db.edit_homework(
                    school,
                    clas,
                    lesson,
                    homework
                )
                db.edit_upd_date(
                    school,
                    clas,
                    lesson,
                    upd_date)
            else:
                db.add_lesson_with_homework(lesson, school, clas, homework, upd_date)
            db.commit()

            await message.answer('Ты успешно обновил дз', keyboard=keyboard)
            logging.info(f'{message.peer_id}: I sent a success')

    except TypeError:
        await message.answer(f'Человек не зарегистрирован!')
        if 'yes_update_homework_' in message.payload:
            await bp.api.messages.send(message=f'Ты не зарегистрирован! \nНапиши "Начать"', user_id=user_id, keyboard=keyboard, random_id=0)
        return

    except Exception as e:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer(f'Произошла ошибка\n{e} \nСообщи админу')
        if 'yes_update_homework_' in message.payload:
           await bp.api.messages.send(message=f'Произошла ошибка\n{e} \nСообщи админу', user_id=user_id, keyboard=keyboard, random_id=0)
        return

    # Если одобрили запрос на обновлние дз
    if message.payload and 'yes_update_homework_' in message.payload:
        await bp.api.messages.send(message='Админ одобрил вашу заявку на обновление дз.', user_id=user_id, keyboard=keyboard, random_id=0)
        await bp.api.messages.send(message=f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', user_id=user_id, keyboard=keyboard, random_id=0)
    
    
    users_with_notification = db.get_accounts_homework_notification()
    chats_with_notification = db.get_chats_homework_notification()
    for i in users_with_notification:
        i_id = i[0]
        if db.get_account_school(i_id) == school:
            if db.get_account_class(i_id) == clas:
                await bp.api.messages.send(message=f'Новое домашнее задание по {lesson}!\nБыло обновлено: {upd_date}\nЗадание: {homework}', user_id=i_id, random_id=0)
                await asyncio.sleep(1)

    for i in chats_with_notification:
        i_id = i[0]
        if db.get_chat_school(i_id) == school:
            if db.get_chat_class(i_id) == clas:
                await bp.api.messages.send(message=f'Новое домашнее задание по {lesson}!\nБыло обновлено: {upd_date}\nЗадание: {homework}', peer_id=2000000000+i_id, random_id=0)
                await asyncio.sleep(1)


    
    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent a success')




@bp.on.chat_message(state=HomeworkData.homework)
async def chat_edit_hamework(message: Message):
    logging.info(f'{message.peer_id}: Im at the end of update_homework')
    chat_id = message.chat_id
    
    if message.payload is None: # если человек попал в этот стейт прямиком из указания дз (у админа не спрашивалось разрешение)
        ctx.set('homework', message.text)# Загружаем во временное хранилище дз

    keyboard = Keyboard()
    keyboard.add(Text("Все дз на 1 день", {'cmd': 'keyboard_homework_for_day'}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()

    lessons = db.get_lessons_with_homework(
        db.get_chat_school(chat_id),
        db.get_chat_class(chat_id)
    )
    counter = 1
    for i in lessons:
        if counter == 4: 
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "homework"}))
        counter += 1

    keyboard.row()
    keyboard.add(Text('Обновить', {"cmd": "keyboard_update_homework"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)


    lesson = ctx.get('lesson') # Берем из временного хранилища урок
    homework = ctx.get('homework') # Берем из временного хранилища дз

    # Если в обнове дз отказали
    if message.payload and 'no_update_homework_' in message.payload:
        await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
        user_id = int(message.payload[28:-2])

        #try:
        await bp.api.messages.send(message=f'Администратор отказал вам в измение дз по {lesson} на:\n{homework}', user_id=user_id, keyboard=keyboard, random_id=0)
        #except VKAPIError[901] as e:
        #    await message.answer("не могу отправить сообщение из-за настроек приватности")
        logging.info(f'{message.peer_id}: I sent a refusal')
        await message.answer('Ты отказал человеку в изменение дз.')
        return

    peer_id = message.peer_id
    chat_id = message.chat_id

    await bp.state_dispenser.delete(peer_id) # Удаляем цепочку

    upd_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}'
    school = db.get_chat_school(chat_id)
    clas = db.get_chat_class(chat_id)
    try:
        if (lesson,) in lessons:
            db.edit_homework(
                school,
                clas,
                lesson,
                homework
            )
            db.edit_upd_date(
                school,
                clas,
                lesson,
                upd_date
            )
        else:
            db.add_lesson_with_homework(lesson, school, clas, homework, upd_date)
        db.commit()

        await message.answer('Ты успешно обновил дз')
        logging.info(f'{message.peer_id}: I sent a success')

    except Exception as e:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer(f'Произошла ошибка\n{e} Сообщи админу')

    users_with_notification = db.get_accounts_homework_notification()
    chats_with_notification = db.get_chats_homework_notification()
    for i in users_with_notification:
        i_id = i[0]
        if db.get_account_school(i_id) == school:
            if db.get_account_class(i_id) == clas:
                await bp.api.messages.send(message=f'Новое домашнее задание по {lesson}!\nБыло обновлено: {upd_date}\nЗадание: {homework}', user_id=i_id, random_id=0)
                await asyncio.sleep(1)

    for i in chats_with_notification:
        i_id = i[0]
        if db.get_chat_school(i_id) == school:
            if db.get_chat_class(i_id) == clas:
                await bp.api.messages.send(message=f'Новое домашнее задание по {lesson}!\nБыло обновлено: {upd_date}\nЗадание: {homework}', peer_id=2000000000+i_id, random_id=0)
                await asyncio.sleep(1)

    await message.answer(f'Урок: {lesson} \nБыло обновлено: {upd_date} \nЗадание: {homework}', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent a success')