from database.main import Database
from database.methods.get import get_student_by_vk_id, get_student_by_telegram_id, get_chat_by_telegram_id, get_chat_by_vk_id
from database.models import Chat, Homework, Schedule, Student




# ```````````````````````````````````````````````STUDENTS`````````````````````````````````````````````````````````

def edit_student_vk_id(telegram_id: int, new_vk_id: str) -> None:
    Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.vk_id: new_vk_id})
    Database().session.commit()

def edit_student_telegram_id(vk_id: int, new_telegram_id: str) -> None:
    Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.telegram_id: new_telegram_id})
    Database().session.commit()

def switch_student_admin(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
        if student:
            student.isAdmin = not student.isAdmin
            Database().session.commit()
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
        if student:
            student.isAdmin = not student.isAdmin
            Database().session.commit()

def edit_student_login(vk_id: int = None, telegram_id: int = None, new_login: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.login: new_login})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.login: new_login})
        Database().session.commit()

def edit_student_password(vk_id: int = None, telegram_id: int = None, new_password: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.password: new_password})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.password: new_password})
        Database().session.commit()

def edit_student_link(vk_id: int = None, telegram_id: int = None, new_link: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.link: new_link})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.link: new_link})
        Database().session.commit()

def edit_student_school(vk_id: int = None, telegram_id: int = None, new_school: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.school: new_school})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.school: new_school})
        Database().session.commit()

def edit_student_clas(vk_id: int = None, telegram_id: int = None, new_clas: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.clas: new_clas})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.clas: new_clas})
        Database().session.commit()

def edit_student_studentId(vk_id: int = None, telegram_id: int = None, new_studentId: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.studentId: new_studentId})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.studentId: new_studentId})
        Database().session.commit()

def switch_student_mark_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
        if student:
            student.mark_notification = not student.mark_notification
            Database().session.commit()
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
        if student:
            student.mark_notification = not student.mark_notification
            Database().session.commit()

def switch_student_announcements_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
        if student:
            student.announcements_notification = not student.announcements_notification
            Database().session.commit()
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
        if student:
            student.announcements_notification = not student.announcements_notification
            Database().session.commit()

def switch_student_schedule_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
        if student:
            student.schedule_notification = not student.schedule_notification
            Database().session.commit()
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
        if student:
            student.schedule_notification = not student.schedule_notification
            Database().session.commit()

def switch_student_homework_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        student = get_student_by_telegram_id(telegram_id)
        if student:
            student.homework_notification = not student.homework_notification
            Database().session.commit()
    elif vk_id:
        student = get_student_by_vk_id(vk_id)
        if student:
            student.homework_notification = not student.homework_notification
            Database().session.commit()

def edit_student_old_mark(vk_id: int = None, telegram_id: int = None, new_old_mark: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.old_mark: new_old_mark})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.old_mark: new_old_mark})
        Database().session.commit()

def edit_student_old_announcements(vk_id: int = None, telegram_id: int = None, new_old_announcements: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.old_announcements: new_old_announcements})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.old_announcements: new_old_announcements})
        Database().session.commit()

def edit_student_correction_lesson(vk_id: int = None, telegram_id: int = None, new_correction_lesson: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.correction_lesson: new_correction_lesson})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.correction_lesson: new_correction_lesson})
        Database().session.commit()

def edit_student_correction_mark(vk_id: int = None, telegram_id: int = None, new_correction_mark: str = None) -> None:
    if telegram_id:
        Database().session.query(Student).filter(Student.telegram_id == telegram_id).update(values={Student.correction_mark: new_correction_mark})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Student).filter(Student.vk_id == vk_id).update(values={Student.correction_mark: new_correction_mark})
        Database().session.commit()



# `````````````````````````````````````````````````CHATS```````````````````````````````````````````````````````````

def edit_chat_vk_id(telegram_id: int, new_vk_id: str) -> None:
    Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.vk_id: new_vk_id})
    Database().session.commit()

def edit_chat_telegram_id(vk_id: int, new_telegram_id: str) -> None:
    Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.telegram_id: new_telegram_id})
    Database().session.commit()

def edit_chat_login(vk_id: int = None, telegram_id: int = None, new_login: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.login: new_login})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.login: new_login})
        Database().session.commit()

def edit_chat_login(vk_id: int = None, telegram_id: int = None, new_login: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.login: new_login})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.login: new_login})
        Database().session.commit()

def edit_chat_password(vk_id: int = None, telegram_id: int = None, new_password: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.password: new_password})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.password: new_password})
        Database().session.commit()

def edit_chat_link(vk_id: int = None, telegram_id: int = None, new_link: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.link: new_link})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.link: new_link})
        Database().session.commit()

def edit_chat_school(vk_id: int = None, telegram_id: int = None, new_school: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.school: new_school})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.school: new_school})
        Database().session.commit()

def edit_chat_clas(vk_id: int = None, telegram_id: int = None, new_clas: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.clas: new_clas})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.clas: new_clas})
        Database().session.commit()

def edit_chat_studentId(vk_id: int = None, telegram_id: int = None, new_studentId: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.studentId: new_studentId})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.studentId: new_studentId})
        Database().session.commit()

def switch_chat_mark_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        chat = get_chat_by_telegram_id(telegram_id)
        if chat:
            chat.mark_notification = not chat.mark_notification
            Database().session.commit()
    elif vk_id:
        chat = get_chat_by_vk_id(vk_id)
        if chat:
            chat.mark_notification = not chat.mark_notification
            Database().session.commit()

def switch_chat_announcements_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        chat = get_chat_by_telegram_id(telegram_id)
        if chat:
            chat.announcements_notification = not chat.announcements_notification
            Database().session.commit()
    elif vk_id:
        chat = get_chat_by_vk_id(vk_id)
        if chat:
            chat.announcements_notification = not chat.announcements_notification
            Database().session.commit()

def switch_chat_schedule_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        chat = get_chat_by_telegram_id(telegram_id)
        if chat:
            chat.schedule_notification = not chat.schedule_notification
            Database().session.commit()
    elif vk_id:
        chat = get_chat_by_vk_id(vk_id)
        if chat:
            chat.schedule_notification = not chat.schedule_notification
            Database().session.commit()

def switch_chat_homework_notification(vk_id: int = None, telegram_id: int = None) -> None:
    if telegram_id:
        chat = get_chat_by_telegram_id(telegram_id)
        if chat:
            chat.homework_notification = not chat.homework_notification
            Database().session.commit()
    elif vk_id:
        chat = get_chat_by_vk_id(vk_id)
        if chat:
            chat.homework_notification = not chat.homework_notification
            Database().session.commit()

def edit_chat_old_mark(vk_id: int = None, telegram_id: int = None, new_old_mark: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.old_mark: new_old_mark})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.old_mark: new_old_mark})
        Database().session.commit()

def edit_chat_old_announcements(vk_id: int = None, telegram_id: int = None, new_old_announcements: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.old_announcements: new_old_announcements})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.old_announcements: new_old_announcements})
        Database().session.commit()

def edit_chat_correction_lesson(vk_id: int = None, telegram_id: int = None, new_correction_lesson: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.correction_lesson: new_correction_lesson})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.correction_lesson: new_correction_lesson})
        Database().session.commit()

def edit_chat_correction_mark(vk_id: int = None, telegram_id: int = None, new_correction_mark: str = None) -> None:
    if telegram_id:
        Database().session.query(Chat).filter(Chat.telegram_id == telegram_id).update(values={Chat.correction_mark: new_correction_mark})
        Database().session.commit()
    elif vk_id:
        Database().session.query(Chat).filter(Chat.vk_id == vk_id).update(values={Chat.correction_mark: new_correction_mark})
        Database().session.commit()



# `````````````````````````````````````````````````````SCHEDULE```````````````````````````````````````````````````


def edit_schedule_photo(school: str, clas: str, day: str, new_photo: str) -> None:
    Database().session.query(Schedule).filter(Schedule.school == school, Schedule.clas == clas, Schedule.day == day).update(values={Schedule.photo: new_photo})
    Database().session.commit()



# `````````````````````````````````````````````````````HOMEWORKS``````````````````````````````````````````````````

def edit_homework(lesson: str, school: str, clas: str, new_homework: str) -> None:
    Database().session.query(Homework).filter(Homework.lesson == lesson, Homework.school == school, Homework.clas == clas).update(values={Homework.homework: new_homework})
    Database().session.commit()

def edit_homework_upd_date(lesson: str, school: str, clas: str, new_upd_date: str) -> None:
    Database().session.query(Homework).filter(Homework.lesson == lesson, Homework.school == school, Homework.clas == clas).update(values={Homework.upd_date: new_upd_date})
    Database().session.commit()