from database.main import Database
from database.methods.get import get_student_by_telegram_id, get_student_by_vk_id, get_chat_by_telegram_id, get_chat_by_vk_id, get_homework, get_schedule


def delete_student(vk_id: int = None, telegram_id: int = None):
    session = Database().session
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
    
    if student:
        session.delete(student)
        session.commit()


def delete_chat(vk_id: int = None, telegram_id: int = None):
    session = Database().session
    if telegram_id:
        chat = get_chat_by_telegram_id(telegram_id)
    elif vk_id:
        chat = get_chat_by_vk_id(vk_id)
    
    if chat:
        session.delete(chat)
        session.commit()


def delete_schedule(school: str, clas: str, day: str):
    session = Database().session
    schedule = get_schedule(school, clas, day)
    
    if schedule:
        session.delete(schedule)
        session.commit()


def delete_homework(lesson: str, school: str, clas: str):
    session = Database().session
    homework = get_homework(lesson, school, clas)
    
    if homework:
        session.delete(homework)
        session.commit()