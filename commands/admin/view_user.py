from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts



bp = Blueprint('view_user')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"view_')
async def view_user(message: Message, userId=None):
    logging.info(f'{message.peer_id}: I get view_user')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    if db.get_account_isAdmin(user_id) == 0:
        await message.answer('У тебя нет админских прав!')
        return
    
    user_id = int(message.payload[13:-2])
    user = db.get_account_all_with_id(user_id)
    data_from_vk = await bp.api.users.get(user_id)

    last_name = data_from_vk[0].last_name
    first_name = data_from_vk[0].first_name
    login = user[0][1]
    password = user[0][2]
    studentId = user[0][3]
    isFirstLogin = user[0][4]
    week = user[0][5]
    day = user[0][6]
    lesson = user[0][7]
    correctData = user[0][8]
    link = user[0][9]
    school = user[0][10]
    clas = user[0][11]
    mark_notification = user[0][12]
    announcements_notification = user[0][13]
    schedule_notification = user[0][14]
    homework_notification = user[0][15]
    old_mark = user[0][16]
    old_announcements = user[0][17]
    correction_lesson = user[0][18]
    correction_mark = user[0][19]
    isAdmin = user[0][20]

    await message.answer(
        f'''
        Имя: {first_name}
        Фаимилия: {last_name}
        Логин: {login}
        Пароль: {password}
        studentId: {studentId}
        isFirstLogin: {isFirstLogin}
        week: {week}
        day: {day}
        lesson: {lesson}
        correctData: {correctData}
        link: {link}
        school: {school}
        clas: {clas}
        mark_notification: {mark_notification}
        announcements_notification: {announcements_notification}
        schedule_notification: {schedule_notification}
        homework_notification: {homework_notification}
        old_mark: {old_mark}
        old_announcements: {old_announcements}
        correction_lesson: {correction_lesson}
        correction_mark: {correction_mark}
        isAdmin : {isAdmin}
        '''
    )