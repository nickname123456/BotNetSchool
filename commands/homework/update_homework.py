from vkbottle import Keyboard, KeyboardButtonColor, Text, CtxStorage, BaseStateGroup
from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from datetime import datetime
import logging
import asyncio
from commands.homework.keyboard_homework import private_keyboard_homework


bp = Blueprint('update_homework') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр


ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class HomeworkData(BaseStateGroup):
    lesson = 20
    homework = 21


@bp.on.private_message(payload={'cmd': 'keyboard_update_homework'})
async def private_keyboard_update_homework(message: Message):
    logging.info(f'{message.peer_id}: I get keyboard_update_homework')
    userId = message.from_id # ID юзера

    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson) # Говорим, что следующий шаг - выбор урока

    keyboard = Keyboard()

    lessons = db.get_lessons_with_homework( # Получаем уроки
        db.get_account_school(userId),
        db.get_account_class(userId)
    )
    counter = 1
    for i in lessons: # Перебираем уроки
        if counter == 4: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[0], {"cmd": "update_homework"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой урок хотите изменить дз? Если для нужного предмета нет кнопки, то просто напиши название.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send list of lessons')


@bp.on.chat_message(payload={'cmd': 'keyboard_update_homework'})
async def chat_keyboard_update_homework(message: Message):
    await message.answer('❌Доступно только в л/с!')




@bp.on.private_message(state=HomeworkData.lesson)
async def get_new_homework(message: Message):
    logging.info(f'{message.peer_id}: I get lesson in update_homework')
    if len(message.text) <= 40:
        ctx.set('lesson', message.text) # Загружаем во временное хранилище урок
    else:
        return '❌Название урока не может быть больше 40 символов! \n🤔Попробуй еще раз'

    await bp.state_dispenser.set(message.peer_id, HomeworkData.homework)
    
    logging.info(f'{message.peer_id}: I sent a question about homework')
    return '💬Введите задание'




@bp.on.private_message(state=HomeworkData.homework)
async def private_edit_hamework(message: Message):
    logging.info(f'{message.peer_id}: Im at the end of update_homework')
    userId = message.from_id # ID юзера

    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку

    lesson = ctx.get('lesson') # Берем из временного хранилища урок
    homework = message.text # Берем дз
    upd_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}'
    lessons = db.get_lessons_with_homework(
        db.get_account_school(userId),
        db.get_account_class(userId)
    )
    
    try:
        school = db.get_account_school(userId)
        clas = db.get_account_class(userId)

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

        await message.answer('✅Вы успешно обновили дз')
        await private_keyboard_homework(message)
        logging.info(f'{message.peer_id}: I sent a success')

    except TypeError:
        await message.answer(f'❌Ты не зарегистрирован! \n🤔Напиши "Начать"')
        return

    except Exception as e:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer(f'❌Произошла ошибка❌\n{e} \n❌Сообщи админу❌')
        return
    
    users_with_notification = db.get_accounts_homework_notification()
    chats_with_notification = db.get_chats_homework_notification()
    for i in users_with_notification:
        i_id = i[0]
        if db.get_account_school(i_id) == school:
            if db.get_account_class(i_id) == clas:
                await bp.api.messages.send(message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}', user_id=i_id, random_id=0)
                await asyncio.sleep(1)

    for i in chats_with_notification:
        i_id = i[0]
        if db.get_chat_school(i_id) == school:
            if db.get_chat_class(i_id) == clas:
                await bp.api.messages.send(message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}', peer_id=2000000000+i_id, random_id=0)
                await asyncio.sleep(1)

    logging.info(f'{message.peer_id}: update_homework is done')