from bs4 import BeautifulSoup as bs4
from typing import List, Dict

user_atributs = ['Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Логин', 'Текущий учебный год', 'Мобильный телефон']

def parseBirthDay(birthDay: str) -> List:
	births_dict = []
	html = bs4(birthDay, 'lxml')
	births = html.find_all('tr')
	for people in births[1:]:
		atributs = people.find_all('td')
		births_dict.append({'name': atributs[3].text, 'date': atributs[2].text, 'role': atributs[1].text})
	return births_dict

def parseUserInfo(html_page: str) -> Dict:
	user_info = {}
	html = bs4(html_page, 'lxml')
	user = html.find_all('div', 'form-group')
	for atribut in user:
		if atribut.text in user_atributs:
			user_info[atribut.text] = str(atribut).split('value=')[1].split('"')[1]
	return user_info

def parseHolidayMonth(html_page: str) -> List:
	holiday_dict = []
	html = bs4(html_page, 'lxml')
	holidays = html.find_all('td', 'vacation-day')
	for holiday in holidays:
		holiday = holiday.text.split('-')
		holiday_dict.append({'date': holiday[0], 'holidays': holiday[1:]})
	return holiday_dict

def parseTerms(html_page: str) -> Dict:
	term_dict = {}
	html = bs4(html_page, 'lxml')
	terms = html.find_all(name = 'select', attrs={'name': 'TERMID'})
	terms = terms[0].find_all('option')
	for term in terms:
		term_dict[term.text] = term.attrs['value']
	return term_dict

def parseTermId(html_page: str) -> List:
	term_list = []
	html = bs4(html_page, 'lxml')
	terms = html.find_all(name = 'select',attrs={'name': 'TERMID'})
	terms = terms[0].find_all('option')
	for term in terms:
		term_list.append(term.attrs['value'])
	return term_list

def parseReportParent(html_page: str) -> Dict:
	report_dict = {'total': {}, 'subjects': {}}
	html = bs4(html_page, 'lxml')
	total = html.find_all('tr', 'totals')
	total = total[0].find_all('td')
	report_dict['total']['5'] = total[1].text
	report_dict['total']['4'] = total[2].text
	report_dict['total']['3'] = total[3].text
	report_dict['total']['2'] = total[4].text
	report_dict['total']['average'] = total[6 if len(total) == 8 else 5].text
	report_dict['total']['average_term'] = total[5 if len(total) == 8 else 6].text
	subjects = html.find_all('tr')
	for subject in subjects[3:][:-10]:
		marks = subject.find_all('td')
		report_dict['subjects'][marks[0].text] = {}
		report_dict['subjects'][marks[0].text]['5'] = marks[1].text
		report_dict['subjects'][marks[0].text]['4'] = marks[2].text
		report_dict['subjects'][marks[0].text]['3'] = marks[3].text
		report_dict['subjects'][marks[0].text]['2'] = marks[4].text
		report_dict['subjects'][marks[0].text]['average'] = marks[6 if len(total) == 8 else 5].text
		report_dict['subjects'][marks[0].text]['term'] = marks[5 if len(total) == 8 else 6].text
	return report_dict

def parseReportTotal(html_page: str) -> Dict:
	report_dict = {'1': {}, '2': {}, '3': {}, '4': {}, 'year': {}}
	html = bs4(html_page, 'lxml')
	subjects = html.find_all('table', 'table-print-num')[0].find_all('tr')
	for subject in subjects[2:]:
		marks = subject.find_all('td')
		report_dict['1'][marks[1].text] = marks[2].text
		report_dict['2'][marks[1].text] = marks[3].text
		report_dict['3'][marks[1].text] = marks[4].text
		report_dict['4'][marks[1].text] = marks[5].text
		report_dict['year'][marks[1].text] = marks[6].text
	return report_dict

def parseAverageMark(html_page: str) -> Dict:
	report_dict = {'average': {}, 'AverageInClass': {}}
	html = bs4(html_page, 'lxml')
	table = html.find_all('table', 'table-print chart-table chart-bars')[0]
	subjects = table.find_all('tr', 'chart-labels-row')[0].find_all('th')
	for subject in subjects[1:]:
		report_dict['average'][subject.text] = None
		report_dict['AverageInClass'][subject.text] = None
	
	marks = table.find_all('tr', 'text-nowrap chart-data-row')[0].find_all('td')
	counter = 0
	for mark in marks[1:]:
		report_dict['average'][list(report_dict['average'].keys())[counter]] = mark.text
		counter += 1

	marks = table.find_all('tr', 'text-nowrap chart-data-row')[1].find_all('td')
	counter = 0
	for mark in marks[1:]:
		report_dict['AverageInClass'][list(report_dict['AverageInClass'].keys())[counter]] = mark.text
		counter += 1
	
	return report_dict

def parseAverageMarkDyn(html_page: str) -> Dict:
	report_dict = {'average': {}, 'AverageInClass': {}}
	html = bs4(html_page, 'lxml')
	table = html.find_all('table', 'table-print-num chart-table chart-lines')[0]
	periods = table.find_all('tr', 'chart-labels-row')[0].find_all('th')
	for period in periods[1:]:
		report_dict['average'][period.text] = None
		report_dict['AverageInClass'][period.text] = None
	
	marks = table.find_all('tr', 'text-nowrap chart-data-row')[0].find_all('td')
	counter = 0
	for mark in marks[1:]:
		report_dict['average'][list(report_dict['average'].keys())[counter]] = mark.text
		counter += 1

	marks = table.find_all('tr', 'text-nowrap chart-data-row')[1].find_all('td')
	counter = 0
	for mark in marks[1:]:
		report_dict['AverageInClass'][list(report_dict['AverageInClass'].keys())[counter]] = mark.text
		counter += 1
	
	return report_dict

def parseReportStudentAttendanceGrades(html_page: str) -> Dict:
	result = {}
	html = bs4(html_page, 'lxml')
	table = html.find_all('table', 'table-print-num chart-table chart-bars')[0]
	
	months = table.find_all('tr', 'chart-labels-row')[0].find_all('th')
	for month in months[1:]:
		result[month.text] = {'student': None, 'class': None, 'parallel': None}
	
	qualities = table.find_all('tr', 'chart-data-row')[0].find_all('td')
	counter = 0
	for quality in qualities[1:]:
		result[list(result.keys())[counter]]['student'] = quality.text
		counter += 1

	qualities = table.find_all('tr', 'chart-data-row')[1].find_all('td')
	counter = 0
	for quality in qualities[1:]:
		result[list(result.keys())[counter]]['class'] = quality.text
		counter += 1
	
	qualities = table.find_all('tr', 'chart-data-row')[2].find_all('td')
	counter = 0
	for quality in qualities[1:]:
		result[list(result.keys())[counter]]['parallel'] = quality.text
		counter += 1
	
	return result

def parseSubjectId(html_page) -> Dict:
	result = {}
	html = bs4(html_page, 'lxml')
	subjectsId = html.find_all(name = 'select', attrs={'name': 'SCLID'})
	subjectsId = subjectsId[0].find_all('option')
	for subjectId in subjectsId:
		result[subjectId.text] = subjectId.attrs['value']
	return result

def parseClassId(html_page):
	html = bs4(html_page, 'lxml')
	classId = html.find_all(name = 'input', attrs={'name': 'PCLID'})[0].attrs['value']
	return classId