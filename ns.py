from netschoolapi import NetSchoolAPI
import datetime
import html2markdown
import re

def get_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    period = [monday, friday]

    return period


def get_next_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    next_monday = monday + datetime.timedelta(days=7)
    next_friday = friday + datetime.timedelta(days=7)

    period = [next_monday, next_friday]

    return period


def get_back_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    last_monday = monday - datetime.timedelta(days=7)
    last_friday = friday - datetime.timedelta(days=7)

    period = [last_monday, last_friday]

    return period


async def get_diary(login, password, period):
    api = NetSchoolAPI('https://sgo.edu-74.ru')
    await api.login(login, password, 'МАОУ "СОШ № 47 г. Челябинска"')
    diary = await api.diary(period[0], period[1])
    await api.logout()
    return diary


async def get_announcements(login, password, amount):
    api = NetSchoolAPI('https://sgo.edu-74.ru')
    await api.login(login, password, 'МАОУ "СОШ № 47 г. Челябинска"')
    announcements = await api.announcements()
    await api.logout()

    announcements = announcements[:int(amount)]

    if announcements:
        announcement = ''
        result = []
        for i in announcements:
            announcement += f"Дата: {i.post_date.date()}\n{i.name}:\n{i.content}\n"

            clean = re.compile(
                r'(style\W\Wcolor: #[a-z0-9]+;\W)|(\Wspan\W)|(<p>)|(</p>)')
            announcement = re.sub(clean, '', announcement)

            result.append(announcement)



        return result
    else:
        return ['❌Нет объявлений!']
