from . import login, menu, not_found, start, information
from .diary import diary_for_day, keyboard_diary
from .homework import homework, keyboard_homework, update_homework, homework_for_day
from .marks import marks, correction_mark_choice_lesson, correction_mark_choice_mark, correction_mark
from .schedule import keyboard_schedule, schedule_download, schedule_for_day
from .settings import keyboard_announcements_notification, keyboard_mark_notification, keyboard_settings, keyboard_schedule_notification, keyboard_homework_notification
from .announcements import announcements
from .admin import admin_panel, give_adm, all_users, view_user
from .reports import reports, reportTotal, reportAverageMark, parentReport, reportAverageMarkDyn, reportGrades
from .change_anything import change_anything_kb, change_student


bps = [not_found.bp,
       menu.bp,
       login.bp,
       keyboard_diary.bp,
       diary_for_day.bp,
       schedule_download.bp,
       keyboard_schedule.bp,
       schedule_for_day.bp,
       announcements.bp,
       start.bp,
       homework_for_day.bp,
       keyboard_homework.bp,
       homework.bp,
       update_homework.bp,
       marks.bp,
       keyboard_settings.bp,
       keyboard_mark_notification.bp,
       keyboard_announcements_notification.bp,
       keyboard_homework_notification.bp,
       correction_mark_choice_lesson.bp,
       correction_mark_choice_mark.bp,
       correction_mark.bp,
       information.bp,
       keyboard_schedule_notification.bp,
       admin_panel.bp,
       give_adm.bp,
       all_users.bp,
       view_user.bp,
       reports.bp,
       reportTotal.bp,
       reportAverageMark.bp,
       parentReport.bp,
       reportAverageMarkDyn.bp,
       reportGrades.bp,
       change_anything_kb.bp,
       change_student.bp
       ]
