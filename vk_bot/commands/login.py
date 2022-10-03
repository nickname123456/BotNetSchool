from database.methods.update import edit_student_login, edit_student_password, edit_student_studentId, edit_chat_login, edit_chat_password, edit_chat_studentId
from database.methods.get import get_chat_by_vk_id, get_student_by_vk_id
import ns

from vkbottle.bot import Message, Blueprint

import logging


bp = Blueprint('login')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Вход" или нажали на соответствующую кнопку
@bp.on.private_message(text=["Вход <userLogin> <userPassword>", "Вход", 'Войти', 'Войти <userLogin> <userPassword>'])
@bp.on.private_message(payload={'cmd': 'login'})
async def private_login(message: Message, userLogin=None, userPassword=None):
    logging.info(f'{message.peer_id}: I get login')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    userId = message.from_id # ID юзера

    # Если человека нет в бд
    if get_student_by_vk_id(userId) is None:
        logging.info(f'{message.peer_id}: User not in database')
        await message.answer("🤔Так... Смотрю вас еще нет в моей базе данных. Но ничего страшного сейчас все будет!")
        await message.answer('Напишите "Начать"')
        return

    #Если пароль и логин введены
    if userLogin != None and userPassword != None:
        student = get_student_by_vk_id(userId)
        try:
            studentId = await ns.getCurrentStudentId(
                userLogin,
                userPassword,
                student.school,
                student.link
            )
            logging.info(f'{message.peer_id}: Login in NetSchool')
        except:
            logging.exception(f'{message.peer_id}: Exception occurred')
            await message.answer('❌Неправильный логин или пароль!❌')
            return

        #Записать в бд
        edit_student_login(vk_id=userId, new_login=userLogin)
        edit_student_password(vk_id=userId, new_password=userPassword)
        edit_student_studentId(vk_id=userId, new_studentId=studentId)
        logging.info(f'{message.peer_id}: Write new data to database')

    
    student = get_student_by_vk_id(userId)
    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            student.login, 
            student.password, 
            student.school,
            student.link,
            student.studentId
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!❌')
        return

    await message.answer(f'✅{userInfo[0].first_name}, вы успешно зашли в систему под логином: {student.login}')
    logging.info(f'{message.peer_id}: login COMPLETED')




@bp.on.chat_message(text=["Вход <userLogin> <userPassword>", "Вход", 'Войти', 'Войти <userLogin> <userPassword>'])
@bp.on.chat_message(payload={'cmd': 'login'})
async def chat_login(message: Message, userLogin=None, userPassword=None):
    logging.info(f'{message.peer_id}: I get login')
    chat_id = message.chat_id # Чат айди

    # Если чата нет в бд
    if get_chat_by_vk_id(chat_id) is None:
        logging.info(f'{message.peer_id}: Chat not in database')
        await message.answer("🤔Так... Смотрю вас еще нет в моей базе данных. Но ничего страшного сейчас все будет!")
        await message.answer('Напишите "Начать"')
        return

    #Если пароль и логин введены
    if userLogin != None and userPassword != None:
        chat = get_chat_by_vk_id(chat_id)
        try:
            studentId = await ns.getCurrentStudentId(
                userLogin,
                userPassword,
                chat.school,
                chat.link
            )
            logging.info(f'{message.peer_id}: Login in NetSchool')
        except:
            logging.exception(f'{message.peer_id}: Exception occurred')
            await message.answer('❌Неправильный логин или пароль!❌')
            return

        #Записать в бд
        edit_chat_login(vk_id=chat_id, new_login=userLogin)
        edit_chat_password(vk_id=chat_id, new_password=userPassword)
        edit_chat_studentId(vk_id=chat_id, new_studentId=studentId)
        logging.info(f'{message.peer_id}: Write new data to database')

    chat = get_chat_by_vk_id(chat_id)
    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            chat.login, 
            chat.password, 
            chat.school,
            chat.link,
            chat.studentId
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌Неправильный логин или пароль!❌')
        return
    
    await message.answer(f'✅Вы успешно зашли в систему под логином: {chat.login}')
    logging.info(f'{message.peer_id}: login COMPLETED')