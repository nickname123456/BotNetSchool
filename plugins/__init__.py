from . import login, menu, not_found, start
from .diary import diary_for_day, keyboard_diary, lesson_information
from .homework import homework, keyboard_homework, update_homework
from .marks import marks
from .schedule import keyboard_schedule, schedule_download, schedule_for_day
from .settings import keyboard_announcements_notification, keyboard_mark_notification, keyboard_settings, notification
from .announcements import announcements


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
       notification.bp]
