from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_announcements


bp = Blueprint('announcements') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений

db = SQLighter('database.db') # Подключаемся к базеданных


@bp.on.private_message(text=["Объявления <amount>", "Объявления"])
@bp.on.private_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере

    try:
        # Получаем объявления
        announcements = await get_announcements(db.get_account_login(userInfo[0].id),
                                    db.get_account_password(userInfo[0].id),
                                    amount,
                                    db.get_account_school(userInfo[0].id),
                                    db.get_account_link(userInfo[0].id))
    except: # если произошла ошибка
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        return

    # Отправляем каждое объявление в отдельном сообщении
    for i in announcements:
        await message.answer(i)



@bp.on.chat_message(text=["Объявления <amount>", "Объявления"])
@bp.on.chat_message(payload={'cmd': 'announcements'})
async def announcements(message: Message, amount=3):
    chat_id = message.chat_id

    try:
        # Получаем объявления
        announcements = await get_announcements(
                                    db.get_chat_login(chat_id),
                                    db.get_chat_password(chat_id),
                                    amount,
                                    db.get_chat_school(chat_id),
                                    db.get_chat_link(chat_id))
    except: # если произошла ошибка
        await message.answer('К этой беседе не подключен аккаунт. \nДля подключение напишите "Вход <логин> <пароль>"')
        return

    # Отправляем каждое объявление в отдельном сообщении
    for i in announcements:
        await message.answer(i)
