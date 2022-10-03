from database.methods.get import get_student_by_vk_id

from vkbottle.bot import Message, Blueprint
from misc.VKRules import PayloadStarts

import logging



bp = Blueprint('view_user')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts



@bp.on.private_message(PayloadStarts='{"cmd":"view_')
async def view_user(message: Message):
    logging.info(f'{message.peer_id}: I get view_user')
    user_id = message.from_id # ID юзера
    admin = get_student_by_vk_id(user_id)

    # Проверка на админа
    if not admin.isAdmin:
        await message.answer('У тебя нет админских прав!')
        return
    
    user_id = int(message.payload[13:-2]) # ID юзера, которого мы смотрим
    student = get_student_by_vk_id(user_id) # Вся инфа из бд про юзера
    data_from_vk = await bp.api.users.get(user_id) # Вся инфа из ВК про юзера

    last_name = data_from_vk[0].last_name
    first_name = data_from_vk[0].first_name

    await message.answer(
        f'''
Имя: {first_name}
Фаимилия: {last_name}
isAdmin : {student.isAdmin}
Логин: {student.login}
Пароль: {student.password}
studentId: {student.studentId}
link: {student.link}
school: {student.school}
clas: {student.clas}
mark_notification: {student.mark_notification}
announcements_notification: {student.announcements_notification}
schedule_notification: {student.schedule_notification}
homework_notification: {student.homework_notification}
len( old_mark ): {len(eval(student.old_mark))}
len( old_announcements ): {len(eval(student.old_announcements))}
correction_lesson: {student.correction_lesson}
correction_mark: {student.correction_mark}
        '''
    )