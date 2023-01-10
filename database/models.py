from sqlalchemy import Column, Integer, String, Boolean, LargeBinary

from .main import Database


class Student(Database.BASE):
    __tablename__ = 'STUDENTS'

    id = Column(Integer, primary_key=True)
    isAdmin = Column(Boolean, default=False)
    vk_id = Column(Integer)
    telegram_id = Column(Integer)
    login = Column(String)
    password = Column(String)
    link = Column(String)
    school = Column(String)
    clas = Column(String)
    studentId = Column(Integer)
    mark_notification = Column(Boolean, default=True)
    announcements_notification = Column(Boolean, default=True)
    schedule_notification = Column(Boolean, default=True)
    homework_notification = Column(Boolean, default=True)
    old_mark = Column(String, default='[]')
    old_announcements = Column(String, default='[]')
    correction_lesson = Column(String)
    correction_mark = Column(String)
    connect_code = Column(Integer)


class Chat(Database.BASE):
    __tablename__ = 'CHATS'

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer)
    telegram_id = Column(Integer)
    login = Column(String)
    password = Column(String)
    link = Column(String)
    school = Column(String)
    clas = Column(String)
    studentId = Column(Integer)
    mark_notification = Column(Boolean, default=False)
    announcements_notification = Column(Boolean, default=True)
    schedule_notification = Column(Boolean, default=True)
    homework_notification = Column(Boolean, default=True)
    old_mark = Column(String, default='[]')
    old_announcements = Column(String, default='[]')
    correction_lesson = Column(String)
    correction_mark = Column(String)
    connect_code = Column(Integer)


class Schedule(Database.BASE):
    __tablename__ = 'SCHEDULE'

    id = Column(Integer, primary_key=True)
    school = Column(String)
    clas = Column(String)
    day = Column(String)
    photo = Column(LargeBinary)


class Homework(Database.BASE):
    __tablename__ = 'HOMEWORKS'

    id = Column(Integer, primary_key=True)
    lesson = Column(String)
    school = Column(String)
    clas = Column(String)
    homework = Column(String)
    upd_date = Column(String)


def register_models():
    Database.BASE.metadata.create_all(Database().engine)