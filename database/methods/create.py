import sqlalchemy.exc

from database.main import Database
from database.models import Student, Chat, Homework, Schedule


def create_student(vk_id: int = None, telegram_id: int = None) -> None:
    session = Database().session
    if vk_id:
        try:
            session.query(Student.vk_id).filter(Student.vk_id == vk_id).one()
        except sqlalchemy.exc.NoResultFound:
            session.add(Student(vk_id=vk_id))
            session.commit()
    elif telegram_id:
        try:
            session.query(Student.telegram_id).filter(Student.telegram_id == telegram_id).one()
        except sqlalchemy.exc.NoResultFound:
            session.add(Student(telegram_id=telegram_id))
            session.commit()


def create_chat(vk_id: int = None, telegram_id: int = None) -> None:
    session = Database().session
    if vk_id:
        try:
            session.query(Chat.vk_id).filter(Chat.vk_id == vk_id).one()
        except sqlalchemy.exc.NoResultFound:
            session.add(Chat(vk_id=vk_id))
            session.commit()
    elif telegram_id:
        try:
            session.query(Chat.telegram_id).filter(Chat.telegram_id == telegram_id).one()
        except sqlalchemy.exc.NoResultFound:
            session.add(Chat(telegram_id=telegram_id))
            session.commit()


def create_schedule(school: str, clas: str, day: str, photo: str) -> None:
    session = Database().session
    try:
        session.query(Schedule).filter(Schedule.school == school, Schedule.clas == clas, Schedule.day == day).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(Schedule(school=school, clas=clas, day=day, photo=photo))
        session.commit()


def create_homework(lesson: str, school: str, clas: str, homework: str, upd_date: str) -> None:
    session = Database().session
    try:
        session.query(Homework).filter(Homework.lesson == lesson, Homework.school == school, Homework.clas == clas).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(Homework(lesson = lesson, school= school, clas = clas, homework = homework, upd_date = upd_date))
        session.commit()