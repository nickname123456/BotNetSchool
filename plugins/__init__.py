from . import login, menu, not_found, start, information
from .diary import diary_for_day, keyboard_diary, lesson_information
from .homework import homework, keyboard_homework, update_homework, homework_for_day
from .marks import marks, correction_mark_choice_lesson, correction_mark_choice_mark, correction_mark
from .schedule import keyboard_schedule, schedule_download, schedule_for_day
from .settings import keyboard_announcements_notification, keyboard_mark_notification, keyboard_settings, keyboard_schedule_notification
from .announcements import announcements
from .admin import admin_panel
from .reports import reports, reportTotal, reportAverageMark, parentReport


bps = [not_found.bp,
       menu.bp,
       login.bp,
       keyboard_diary.bp,
       diary_for_day.bp,
       lesson_information.bp,
       schedule_download.bp,
       keyboard_schedule.bp,
       schedule_for_day.bp,
       announcements.bp,
       start.bp,
       keyboard_homework.bp,
       homework.bp,
       update_homework.bp,
       marks.bp,
       keyboard_settings.bp,
       keyboard_mark_notification.bp,
       keyboard_announcements_notification.bp,
       correction_mark_choice_lesson.bp,
       correction_mark_choice_mark.bp,
       correction_mark.bp,
       information.bp,
       homework_for_day.bp,
       keyboard_schedule_notification.bp,
       admin_panel.bp,
       reports.bp,
       reportTotal.bp,
       reportAverageMark.bp,
       parentReport.bp
       ]
