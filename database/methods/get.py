from sqlalchemy import exc

from database.main import Database
from database.models import Student, Chat, Schedule, Homework


def get_student_by_id(_id: int) -> Student:
    try:
        return Database().session.query(Student).filter(Student.id == _id).one()
    except exc.NoResultFound:
        return None

def get_student_by_telegram_id(telegram_id: int) -> Student:
    try:
        return Database().session.query(Student).filter(Student.telegram_id == telegram_id).one()
    except exc.NoResultFound:
        return None

def get_student_by_vk_id(vk_id: int) -> Student:
    try:
        return Database().session.query(Student).filter(Student.vk_id == vk_id).one()
    except exc.NoResultFound:
        return None


def get_all_students() -> list[Student]:
    try:
        return Database().session.query(Student).all()
    except exc.NoResultFound:
        return None

def get_all_chats() -> list[Chat]:
    try:
        return Database().session.query(Chat).all()
    except exc.NoResultFound:
        return None


def get_students_with_admin() -> list[Student]:
    try:
        return Database().session.query(Student).filter(Student.isAdmin == True).all()
    except exc.NoResultFound:
        return None


def get_all_classes_by_school(school) -> list:
    try:
        clas_from_students = Database().session.query(Student.clas).filter(Student.school == school).all()
        clas_from_chats = Database().session.query(Chat.clas).filter(Chat.school == school).all()
        return clas_from_students + clas_from_chats
    except exc.NoResultFound:
        return None


def get_students_with_mark_notification() -> list[Student]:
    try:
        return Database().session.query(Student).filter(Student.mark_notification == True).all()
    except exc.NoResultFound:
        return None

def get_chats_with_mark_notification() -> list[Chat]:
    try:
        return Database().session.query(Chat).filter(Chat.mark_notification == True).all()
    except exc.NoResultFound:
        return None


def get_students_with_announcements_notification() -> list[Student]:
    try:
        return Database().session.query(Student).filter(Student.announcements_notification == True).all()
    except exc.NoResultFound:
        return None

def get_chats_with_announcements_notification() -> list[Chat]:
    try:
        return Database().session.query(Chat).filter(Chat.announcements_notification == True).all()
    except exc.NoResultFound:
        return None


def get_students_with_schedule_notification() -> list[Student]:
    try:
        return Database().session.query(Student).filter(Student.schedule_notification == True).all()
    except exc.NoResultFound:
        return None

def get_chats_with_schedule_notification() -> list[Chat]:
    try:
        return Database().session.query(Chat).filter(Chat.schedule_notification == True).all()
    except exc.NoResultFound:
        return None


def get_students_with_homework_notification() -> list[Student]:
    try:
        return Database().session.query(Student).filter(Student.homework_notification == True).all()
    except exc.NoResultFound:
        return None

def get_chats_with_homework_notification() -> list[Chat]:
    try:
        return Database().session.query(Chat).filter(Chat.homework_notification == True).all()
    except exc.NoResultFound:
        return None




def get_chat_by_telegram_id(telegram_id: int) -> Chat:
    try:
        return Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).one()
    except exc.NoResultFound:
        return None

def get_chat_by_vk_id(vk_id: int) -> Chat:
    try:
        return Database().session.query(Chat).filter(Chat.vk_id == vk_id).one()
    except exc.NoResultFound:
        return None


def get_schedule(school: str, clas: str, day: str) -> Schedule:
    try:
        return Database().session.query(Schedule).filter(Schedule.school == school, Schedule.clas == clas, Schedule.day == day).one()
    except exc.NoResultFound:
        return None


def get_homework(lesson: str, school: str, clas: str) -> Homework:
    try:
        return Database().session.query(Homework).filter(Homework.lesson == lesson, Homework.school == school, Homework.clas == clas).one()
    except exc.NoResultFound:
        return None