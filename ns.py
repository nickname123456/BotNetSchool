from netschoolapi import NetSchoolAPI
import datetime
import re
import html2markdown
from settings import lessons_and_their_smiles


async def get_student(url, login, password, school, studentId):
	api = NetSchoolAPI(url)
	student = await api.login(login,password,school, studentId)
	await api.logout()
	return student

    
async def get_countries(url):
	api = NetSchoolAPI(url)
	result = await api.countries()
	await api.close()
	return result
    
async def get_provinces(url, countryId):
	api = NetSchoolAPI(url)
	result = await api.provinces(countryId)
	await api.close()
	return result
    
async def get_cities(url, countryId, provincesId):
	api = NetSchoolAPI(url)
	result = await api.cities(countryId, provincesId)
	await api.close()
	return result
    
async def get_school(url, countryId = None, provincesId = None, cityId = None):
	api = NetSchoolAPI(url)
	result = await api.schools(countryId, provincesId, cityId)
	await api.close()
	return result



# Вход в сго
async def login(login, password, school, link, studentId = None):
    api = NetSchoolAPI(link)
    await api.login(
        login,
        password,
        school,
        studentId)
    await api.logout()


# Получить текущую неделю
def get_week():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    saturday = monday + datetime.timedelta(days=5)

    week = [monday, saturday]

    return week


# Получить следующую неделю
def get_next_week():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())

    next_monday = monday + datetime.timedelta(days=7)
    next_saturday = next_monday + datetime.timedelta(days=5)

    week = [next_monday, next_saturday]

    return week


# Получить предыдущую неделю
def get_back_week():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())

    last_monday = monday - datetime.timedelta(days=7)
    last_saturday = last_monday + datetime.timedelta(days=5)

    week = [last_monday, last_saturday]

    return week


# Получить дневник
async def get_diary(login, password, period, school, link, studentId):
    api = NetSchoolAPI(link)
    await api.login(
        login,
        password,
        school,
        studentId)
    diary = await api.diary(period[0], period[1])
    await api.logout()
    return diary


# Получить объявления
async def get_announcements(login, password, amount, school, link, studentId):
    api = NetSchoolAPI(link) # Логинимся в СГО
    await api.login(
        login,
        password,
        school,
        studentId)
    announcements = await api.announcements() # Получаем объявления
    await api.logout() # Выходим из СГО

    announcements = announcements[:int(amount)] # Обрезаем только нужные объявления

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



async def get_marks(login, password, school, url, studentId, subject = None, onlySubjects: bool = None):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login,password,school,studentId)
    period = await api.get_period() # Получаем текущий триместр/четверть
    period = period['filterSources'][2]['defaultValue'].split(' - ')
    start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
    end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
    diary = await api.diary(start=start, end=end) # Получаем дневник
    await api.logout() # Выходим из СГО
    # Перебираем оценки
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
    if onlySubjects:
        return list(marks.keys())

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
        
    elif subject == 'all':
        return marks
    else:
        return marks[subject]



async def getMarkNotify(login, password, school, url, oldmarks):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school)
    students = await api.getStudents() # Получаем детей, привязанных к аккаунту СГО
    await api.logout() # Выходим из СГО

    
    marks = []
    for student in students: # Перебираем детей
        studentId = student['studentId']
        studentNick = student['nickName']

        api = NetSchoolAPI(url) # Логинимся в СГО
        await api.login(login, password, school, studentId)
        period = await api.get_period() # Получаем текущий триместр/четверть
        period = period['filterSources'][2]['defaultValue'].split(' - ')
        start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
        end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
        diary = await api.diary(start=start, end=end) # Получаем весь дневник за период/триместр
        await api.logout() # Выходим из СГО

        # Перебираем все оценки
        for days in diary['weekDays']:
            for lesson in days['lessons']:
                if 'assignments' in lesson.keys():
                    for assignment in lesson['assignments']:
                        if 'mark' in assignment.keys() and 'mark' in assignment['mark']:
                            if assignment['mark']['mark']:
                                date = datetime.datetime.strptime(assignment['dueDate'], '%Y-%m-%dT%H:%M:%S')
                                result = html2markdown.convert(f"❗У ученика {studentNick} новая оценка по предмету {lesson['subjectName']}: {assignment['mark']['mark']} за {assignment['assignmentName']}. Дата: {date.day}.{date.month}.{date.year}")
                                clean = re.compile(r'([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                                result = re.sub(clean, '', result)
                                marks.append(result)
    # Смотрим какие оценки новые
    difference = []
    for item in marks:
        try:
            if item not in eval(oldmarks):
                difference.append(item)
        except TypeError:
            if item not in oldmarks:
                difference.append(item)

    return marks, difference




async def getAnnouncementsNotify(login, password, school, url, studentId, old_announcements):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    announcements = await api.announcements() # Получаем все объявления
    await api.logout() # Выходим из СГО

    # Если есть объявления:
    if announcements:
        # Приводим объявления в нужный вид
        announcement = ''
        needed_announcements = []
        for i in announcements:
            announcement = f"❗Новое объявление \nДата: {i['postDate']}\n {i['name']}: {i['description']}"

            announcement = re.sub(r'\<[^>]*\>', '', announcement)

            needed_announcements.append(announcement)
    # Смотрим какие объявления новые
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




async def correction_mark(login, password, school, url, studentId, subject, mark):
    all_marks = await get_marks(login, password, school, url, studentId, subject) # Получаем текущие оценки по этому предмету

    if len(all_marks) != 0: # Если есть оценки
        average_mark = float(round(sum(all_marks) / len(all_marks), 2)) # Считаем ср. балл
    else:
        average_mark = 0.0 # Ср. балл = 0

    lower_threshold = float(mark) - 0.4 # Считаем нижний порог
    len_5 = 0 # Кол-во пятерок
    len_4 = 0 # Кол-во четверок
    len_3 = 0 # Кол-во троек

    if mark == 5: # Если нужна пятерка
        corrective_marks = [5] # Исправлять можно только пятерками
    elif mark == 4: # Если нужна четверка
        corrective_marks = [5,4] # Нужно исправлять пятерками и четверками
    elif mark == 3: # Если нужна тройка
        corrective_marks = [5,4,3] # исправлять можно пятерками, четверками и тройками

    if average_mark >= lower_threshold: # если оценка уже нужная или выше
        return '🤔У вас и так нужная оценка'
    
    for i in corrective_marks: # Перебираем оценки, которыми можно исправлять
        all_marks = await get_marks(login, password, school, url, studentId, subject) # Получаем все текущие оценки

         # Считаем ср. балл
        if len(all_marks) != 0:
            average_mark = float(round(sum(all_marks) / len(all_marks), 2))
        else:
            average_mark = 0.0
        
        while average_mark <= lower_threshold: # Пока ср. балл ниже нужной оценки
            all_marks.append(i) # добавляем ко всем оценкам новую
            average_mark = float(round(sum(all_marks) / len(all_marks), 2)) # Считаем ср. балл

            # Добавляем к кол-во нужных оценок еще одну
            if i == 5:
                len_5 += 1
            elif i == 4:
                len_4 += 1
            elif i == 3:
                len_3 += 1
    
    return f'Для твоей цели нужны такие оценки: \n 5️⃣: {len_5} \nили\n4️⃣: {len_4} \nили\n 3️⃣: {len_3}'



async def getReportTotal(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    reportTotal = await api.reportTotal() # Получаем отчет
    await api.logout() # Выходим из СГО
    result = {}
    # Приводим в нужный вид
    for period in reportTotal.keys():
        if period == 'year': result[period] = f'Оценки за год:'
        else: result[period] = f'Оценки за {period} триместр/четверть:'

        for i in reportTotal[period].keys():
            if i in lessons_and_their_smiles:
                result[period] += f'\n{lessons_and_their_smiles[i]}{i}: {reportTotal[period][i]}'
            else:
                result[period] += f'\n📖{i}: {reportTotal[period][i]}'

    # Предупреждение
    result['Warning'] = '⚠️Внимание⚠️ \nЕсли у вас триместры, то оценки за год стоят под названием "Оценки за 4 триместр/четверть"'
    return result

async def getReportAverageMark(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    reportAverageMark = await api.reportAverageMark() # Получаем отчет
    await api.logout() # Выходим из СГО
    
    # Приводим в нужный вид
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

async def getReportAverageMarkDyn(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    reportAverageMarkDyn = await api.reportAverageMarkDyn() # Получаем отчет
    await api.logout() # Выходим из СГО
    
    # Приводим в нужный вид
    result = []
    for period in reportAverageMarkDyn['average'].keys():
        result.append(f'🙍‍♂Ср. балл ученика за {period}: {reportAverageMarkDyn["average"][period]}')
    for period in reportAverageMarkDyn['AverageInClass'].keys():
        result.append(f'👫Ср. балл класса за {period}: {reportAverageMarkDyn["AverageInClass"][period]}')
    
    return result

async def getParentReport(login, password, school, url, studentId, termId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    parentReport = await api.parentReport(termId) # Получаем отчет
    await api.logout() # Выходим из СГО
    
    result = []
    # Приводим в нужный вид
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

async def getReportGrades(login, password, school, url, studentId, subjectId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    reportGrades = await api.reportStudentAttendanceGrades(subjectId) # Получаем отчет
    await api.logout() # Выходим из СГО

    # Приводим в нужный вид
    result = []
    for i in reportGrades.keys():
        result.append(f'📅Месяц: {i} \n🙍‍♂Ученик: {reportGrades[i]["student"]}% \n👫Среднее по классу: {reportGrades[i]["class"]}% \n👯‍♂Среднее по параллели: {reportGrades[i]["parallel"]}%')
    return result

async def getSubjectsId(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    subjects = await api.getSubjectId() # Получаем ID предмета
    await api.logout() # Выходим из СГО
    return subjects

async def getTerms(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    terms = await api.getTerms() # Получаем все триместры/четверти
    await api.logout() # Выходим из СГО
    return terms

async def getStudents(login, password, school, url, studentId):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    students = await api.getStudents()
    await api.logout() # Выходим из СГО
    return students

async def getCurrentStudentId(login, password, school, url, studentId=None):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    studentId = await api.getCurrentStudentId() # Получаем ID выбранного ребенка
    await api.logout() # Выходим из СГО
    return studentId

async def getSettings(login, password, school, url, studentId, clas):
    api = NetSchoolAPI(url) # Логинимся в СГО
    await api.login(login, password, school, studentId)
    settings = await api.userInfo() # Получаем личную инфу из СГО
    await api.logout() # Выходим из СГО
    result = '🔐Твои личные данные из СГО:\n\n'
    result +=  f'Школа: {school}\n'
    result +=  f'Класс: {clas}\n'
    for key in settings.keys():
        result += f'{key}: {settings[key]}\n'
    return result