from database.methods.get import get_chats_with_homework_notification, get_homework, get_student_by_vk_id, get_students_with_homework_notification
from database.methods.update import edit_homework, edit_homework_upd_date, edit_student_telegram_id, edit_student_vk_id
from database.methods.create import create_homework
from database.methods.delete import delete_chat

from vk_bot.commands.homework.keyboard_homework import private_keyboard_homework
from tg_bot.utils import send_telegram_msg
from settings import tg_token
import ns

from vkbottle import Keyboard, KeyboardButtonColor, Text, CtxStorage, BaseStateGroup, VKAPIError
from vkbottle.bot import Message, Blueprint

import aiogram

from datetime import datetime
import logging
import asyncio


tg_bot = aiogram.Bot(token=tg_token, parse_mode='HTML')

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
    student = get_student_by_vk_id(userId)

    await bp.state_dispenser.set(message.peer_id, HomeworkData.lesson) # Говорим, что следующий шаг - выбор урока

    keyboard = Keyboard()

    lessons = await ns.getSubjectsId(
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId
    )
    counter = 1
    for i in lessons: # Перебираем уроки
        if counter == 4: # Если на строке уже 4 урока, то переходим на след строку
            keyboard.row()
            counter = 1
        keyboard.add(Text(i[:40], {"cmd": f"update_homework_{lessons[i]}"}))
        counter += 1
    
    keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('🤔На какой урок хотите изменить дз?', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I send list of lessons')


@bp.on.chat_message(payload={'cmd': 'keyboard_update_homework'})
async def chat_keyboard_update_homework(message: Message):
    await message.answer('❌Доступно только в л/с!')




@bp.on.private_message(state=HomeworkData.lesson)
async def get_new_homework(message: Message):
    logging.info(f'{message.peer_id}: I get lesson in update_homework')
    ctx.set('lesson', message.payload[24:-2]) # Загружаем во временное хранилище id урока

    await bp.state_dispenser.set(message.peer_id, HomeworkData.homework)
    
    logging.info(f'{message.peer_id}: I sent a question about homework')
    return '💬Введите задание'




@bp.on.private_message(state=HomeworkData.homework)
async def private_edit_hamework(message: Message):
    logging.info(f'{message.peer_id}: Im at the end of update_homework')
    userId = message.from_id # ID юзера
    student = get_student_by_vk_id(userId)

    await bp.state_dispenser.delete(message.peer_id) # Удаляем цепочку
    lessonId = ctx.get('lesson') # Берем из временного хранилища урок
    homework = message.text # Берем дз
    upd_date = f'{datetime.now().hour}:{datetime.now().minute} {datetime.now().day}.{datetime.now().month}.{datetime.now().year}'

    try:
        lessons = await ns.getSubjectsId(
            student.login,
            student.password,
            student.school,
            student.link,
            student.studentId
        )
        lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]

        if get_homework(lesson, student.school, student.clas):
            edit_homework(lesson, student.school, student.clas, homework)
            edit_homework_upd_date(lesson, student.school, student.clas, upd_date)
        else:
            create_homework(lesson, student.school, student.clas, homework, upd_date)

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
    
    # Получаем людей, которые подписаны на уведомленя о дз
    users_with_notification = get_students_with_homework_notification()
    chats_with_notification = get_chats_with_homework_notification()
    for i in users_with_notification:
        telegram_id = i.telegram_id
        vk_id = i.vk_id
        if i.school == student.school: # Если школа совпадает
            if i.clas == student.clas: # Если класс совпадает
                if vk_id: # Если есть аккаунт вк
                    try: # Отправляем уведомление
                        await bp.api.messages.send(message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}', user_id=vk_id, random_id=0)
                    except VKAPIError: # Если не получилось отправить
                        if vk_id and telegram_id: # Если есть аккаунт вк и телеграм
                            await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message='❌Я не могу отправить вам сообщение в ВК, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в телеграмме')
                            edit_student_vk_id(telegram_id=telegram_id, new_vk_id=None) # Удаляем аккаунт вк
                if telegram_id: # Если есть аккаунт телеграм
                    try: # Отправляем уведомление
                        await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                    except aiogram.exceptions.BotBlocked: # Если не получилось отправить
                        if vk_id and telegram_id: # Если есть аккаунт вк и телеграм
                            await bp.api.messages.send(message='❌Я не могу отправить вам сообщение в телеграмме, т.к. вы заблокировали меня. Я буду отправлять вам сообщения только в ВК', user_id=vk_id, random_id=0)
                            edit_student_telegram_id(vk_id=vk_id, new_telegram_id=None) # Удаляем аккаунт телеграм
                await asyncio.sleep(1) # Отдыхаем, чтобы не спамить

    for i in chats_with_notification:
        telegram_id = i.telegram_id
        vk_id = i.vk_id
        if i.school == student.school:  # Если школа совпадает
            if i.clas == student.clas: # Если класс совпадает
                if vk_id: # Если есть аккаунт вк
                    try: # отправляем уведомление
                        await bp.api.messages.send(message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}', peer_id=2000000000+vk_id, random_id=0)
                    except VKAPIError: # Если не получилось отправить
                        delete_chat(vk_id=vk_id) # Удаляем чат из базы данных
                if telegram_id: # Если есть аккаунт телеграм
                    try: # Отправляем уведомление
                        await send_telegram_msg(bot=tg_bot, chat_id=telegram_id, message=f'🔄Новое домашнее задание по {lesson}!\n🆙Было обновлено: {upd_date}\n💬Задание: {homework}')
                    except aiogram.exceptions.BotKicked: # Если не получилось отправить
                        delete_chat(telegram_id=telegram_id) # Удаляем чат из базы данных
                await asyncio.sleep(1) # Отдыхаем, чтобы не спамить

    logging.info(f'{message.peer_id}: update_homework is done')