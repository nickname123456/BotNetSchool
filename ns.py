from netschoolapi import NetSchoolAPI
import datetime
import re



# Вход в сго
async def login(login, password, school, link):
    api = NetSchoolAPI(link)
    await api.login(
        login,
        password,
        school)


# Выход из сго
async def logout(link):
    api = NetSchoolAPI(link)
    await api.logout()


# Получить текущую неделю
def get_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    period = [monday, friday]

    return period


# Получить следующую неделю
def get_next_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    next_monday = monday + datetime.timedelta(days=7)
    next_friday = friday + datetime.timedelta(days=7)

    period = [next_monday, next_friday]

    return period


# Получить предыдущую неделю
def get_back_period():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    last_monday = monday - datetime.timedelta(days=7)
    last_friday = friday - datetime.timedelta(days=7)

    period = [last_monday, last_friday]

    return period


# Получить дневник
async def get_diary(login, password, period, school, link):
    api = NetSchoolAPI(link)
    await api.login(
        login,
        password,
        school)
    diary = await api.diary(period[0], period[1])
    await api.logout()
    return diary


# Получить объявления
async def get_announcements(login, password, amount, school, link):
    api = NetSchoolAPI(link)
    await api.login(
        login,
        password,
        school)
    announcements = await api.announcements()
    await api.logout()

    announcements = announcements[:int(amount)]

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        result = []
        for i in announcements:
            announcement += f"Дата: {i.post_date.date()}\n{i.name}:\n{i.content}\n"

            clean = re.compile(
                r'(style\W\Wcolor: #[a-z0-9]+;\W)|(\Wspan\W)|(<p>)|(</p>)')
            announcement = re.sub(clean, '', announcement)

            result.append(announcement)

        return result
    # Если нет объявлений:
    else:
        return ['❌Нет объявлений!']
