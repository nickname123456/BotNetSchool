from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
import logging
from VKRules import PayloadStarts
import ns


bp = Blueprint('homework') # Объявляем команду
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts




@bp.on.private_message(PayloadStarts='{"cmd":"homework_')
async def private_homework(message: Message):
    logging.info(f'{message.peer_id}: I get homework')
    userId = message.from_id # ID юзера

    lessons = await ns.getSubjectsId(
        db.get_account_login(userId),
        db.get_account_password(userId),
        db.get_account_school(userId),
        db.get_account_link(userId),
        db.get_account_studentId(userId)
    )

    lessonId = message.payload[17:-2]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]
    try:
        # Получаем дз
        homework = db.get_homework(
            db.get_account_school(userId),
            db.get_account_class(userId),
            lesson
        )

        # Получаем дату обновления дз
        upd_date = db.get_upd_date(
            db.get_account_school(userId),
            db.get_account_class(userId),
            lesson
        )
    except TypeError:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')
        return

    await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
    logging.info(f'{message.peer_id}: Send homework')



@bp.on.chat_message(PayloadStarts='{"cmd":"homework_')
async def chat_homework(message: Message):
    logging.info(f'{message.peer_id}: I get homework')
    chat_id = message.chat_id

    lessons = await ns.getSubjectsId(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )

    lessonId = message.payload[17:-2]
    lesson = [lesson for lesson in lessons if lessons[lesson] == lessonId][0]
    try:
        # Получаем дз
        homework = db.get_homework(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson
        )

        # Получаем дату обновления дз
        upd_date = db.get_upd_date(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            lesson
        )
    except TypeError:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('❌К сожалению на этот урок еще нет домашнего задания. \n☺Но вы можете можете сами его записать. Нажмите на кнопку "Обновить"')
        return
    except Exception as e:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer(f'❌Ошибка: {e} \nСообщите администратору!❌')
        return

    await message.answer(f'📚Урок: {lesson} \n🆙Было обновлено: {upd_date} \n💬Задание: {homework}')
    logging.info(f'{message.peer_id}: Send homework')