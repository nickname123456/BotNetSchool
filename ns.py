from netschoolapi import NetSchoolAPI
import datetime
import re
import html2markdown
from settings import lessons_and_their_smiles


async def get_student(url, login, password, school):
	api = NetSchoolAPI(url)
	student = await api.login(login,password,school)
	await api.logout()
	return student

    
async def get_school(url):
	api = NetSchoolAPI(url)
	result = await api.schools()
	await api.close()
	return result



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
            announcement = f"Дата: {i.post_date.date()}\n{i.name}:\n{i.content}\n"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            result.append(announcement)

        return result
    # Если нет объявлений:
    else:
        return ['❌Нет объявлений!']



async def get_marks(login, password, school, url, subject = None):
    api = NetSchoolAPI(url)
    await api.login(login,password,school)
    period = await api.get_period()
    period = period['filterSources'][2]['defaultValue'].split(' - ')
    start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
    end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
    diary = await api.diary(start=start, end=end)
    await api.logout()
    marks = {}
    for days in diary['weekDays']:
        for lesson in days['lessons']:
            if lesson['subjectName'] not in marks.keys():
                marks[lesson['subjectName']] = []
            if 'assignments' in lesson.keys():
                for assignment in lesson['assignments']:
                    if 'mark' in assignment.keys() and 'mark' in assignment['mark']:
                        if assignment['mark']['mark'] != None:
                            marks[lesson['subjectName']].append(assignment['mark']['mark'])

    if subject == None:                     
        result = ''
        for lesson in marks.keys():
            if marks[lesson]:
                marks[lesson] = [mark for mark in marks[lesson] if mark]
                general_sum = round(sum(marks[lesson]) / len(marks[lesson]), 2)
                marks[lesson] = ' '.join(str(e) for e in marks[lesson])
                result += f"\n{lesson}: {marks[lesson]} | {general_sum}"
        if not result:
            result = '❌Нет оценок'
        return result
    else:
        return marks[subject]



async def getMarkNotify(login, password, school, url, oldmarks):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    period = await api.get_period()
    period = period['filterSources'][2]['defaultValue'].split(' - ')
    start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
    end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
    diary = await api.diary(start=start, end=end)
    await api.logout()
    marks = []
    for days in diary['weekDays']:
        for lesson in days['lessons']:
            if 'assignments' in lesson.keys():
                for assignment in lesson['assignments']:
                    if 'mark' in assignment.keys() and 'mark' in assignment['mark']:
                        if assignment['mark']['mark']:
                            date = datetime.datetime.strptime(assignment['dueDate'], '%Y-%m-%dT%H:%M:%S')
                            result = html2markdown.convert(f"Новая оценка по {lesson['subjectName']}: {assignment['mark']['mark']} за {assignment['assignmentName']}. Дата: {date.day}.{date.month}")
                            clean = re.compile(r'([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                            result = re.sub(clean, '', result)
                            marks.append(result)

    difference = []
    for item in marks:
        try:
            if item not in eval(oldmarks):
                difference.append(item)
        except TypeError:
            if item not in oldmarks:
                difference.append(item)

    return marks, difference




async def getAnnouncementsNotify(login, password, school, url, old_announcements):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    announcements = await api.announcements()
    await api.logout()

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        needed_announcements = []
        for i in announcements:
            announcement = "Дата: " + i['postDate'] +"\n"+ i['name'] + ":" + i['description']

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            needed_announcements.append(announcement)

    difference = []
    try:
        for item in needed_announcements:
            if item not in eval(old_announcements):
                difference.append(item)
    except TypeError:
        for item in needed_announcements:
            if item not in old_announcements:
                difference.append(item)

    return needed_announcements, difference




async def correction_mark(login, password, school, url, subject, mark):
    all_marks = await get_marks(login, password, school, url, subject)

    if len(all_marks) != 0:
        average_mark = float(round(sum(all_marks) / len(all_marks), 2))
    else:
        average_mark = 0.0

    lower_threshold = float(mark) - 0.4
    len_5 = 0
    len_4 = 0
    len_3 = 0

    if mark == 5:
        corrective_marks = [5]
    elif mark == 4:
        corrective_marks = [5,4]
    elif mark == 3:
        corrective_marks = [5,4,3]

    if average_mark >= lower_threshold:
        return 'У тебя и так норм оценка'
    
    for i in corrective_marks:
        all_marks = await get_marks(login, password, school, url, subject)

        if len(all_marks) != 0:
            average_mark = float(round(sum(all_marks) / len(all_marks), 2))
        else:
            average_mark = 0.0
        
        while average_mark <= lower_threshold:
            all_marks.append(i)
            average_mark = float(round(sum(all_marks) / len(all_marks), 2))

            if i == 5:
                len_5 += 1
            elif i == 4:
                len_4 += 1
            elif i == 3:
                len_3 += 1
    
    return f'Для твоей цели нужны такие оценки: \n 5️⃣: {len_5} \nили\n4️⃣: {len_4} \nили\n 3️⃣: {len_3}'



async def getReportTotal(login, password, school, url):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    reportTotal = await api.reportTotal()
    result = {}
    for period in reportTotal.keys():
        if period == 'year': result[period] = f'Оценки за год:'
        else: result[period] = f'Оценки за {period} триместр/четверть:'

        for i in reportTotal[period].keys():
            if i in lessons_and_their_smiles:
                result[period] += f'\n{lessons_and_their_smiles[i]}{i}: {reportTotal[period][i]}'
            else:
                result[period] += f'\n📖{i}: {reportTotal[period][i]}'

    result['Warning'] = '⚠️Внимание⚠️ \nЕсли у вас триместры, то оценки за год стоят под названием "Оценки за 4 триместр/четверть"'
    return result

async def getReportAverageMark(login, password, school, url):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    reportAverageMark = await api.reportAverageMark()
    
    result = ['Вот твой средний балл на текущий триместр/четверть:', 'Вот средний балл твоего класса на текущий триместр/четверть:']

    for i in reportAverageMark['average'].keys():
        if i in lessons_and_their_smiles:
            result[0] += f"\n{lessons_and_their_smiles[i]}{i}: {reportAverageMark['average'][i]}"
        else:
            result[0] += f"\n📖{i}: {reportAverageMark['average'][i]}"
    
    for i in reportAverageMark['AverageInClass'].keys():
        if i in lessons_and_their_smiles:
            result[1] += f"\n{lessons_and_their_smiles[i]}{i}: {reportAverageMark['AverageInClass'][i]}"
        else:
            result[1] += f"\n📖{i}: {reportAverageMark['AverageInClass'][i]}"

    return result

async def getParentReport(login, password, school, url):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    parentReport = await api.parentReport()
    
    result = []

    for subject in parentReport['subjects'].keys():
        if subject in lessons_and_their_smiles:
            result.append(f"{lessons_and_their_smiles[subject]}{subject}:")
        else:
            result.append(f"👨‍🎓{subject}:")
        for mark in parentReport['subjects'][subject].keys():
            if mark != 'average' and mark != 'term':
                result[-1] += f"\nОценок '{mark}': {parentReport['subjects'][subject][mark]}"
        result[-1] += f"\nСредний балл: {parentReport['subjects'][subject]['average']}"
        result[-1] += f"\nИтог: {parentReport['subjects'][subject]['term']}"

    result.append('📊Итого по всем предметам:')
    for mark in parentReport['total'].keys():
        if mark != 'average' and mark != 'average_term':
            result[-1] += f"\nОценок '{mark}': {parentReport['total'][mark]}"
    result[-1] += f"\nСредний балл: {parentReport['total']['average']}"
    result[-1] += f"\nИтог: {parentReport['total']['average_term']}"

    return result



async def getSettings(login, password, school, url, clas):
    api = NetSchoolAPI(url)
    await api.login(login, password, school)
    settings = await api.userInfo()
    result = '🔐Твои личные данные из СГО:\n\n'
    result +=  f'Школа: {school}\n'
    result +=  f'Класс: {clas}\n'
    for key in settings.keys():
        result += f'{key}: {settings[key]}\n'
    return result