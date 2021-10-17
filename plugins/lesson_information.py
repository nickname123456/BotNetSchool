from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from ns import get_diary
import netschoolapi


bp = Blueprint('diary_for_day')
db = SQLighter('database.db')







@bp.on.message(payload=[{'cmd': 'lesson_information_0'},
                         {'cmd': 'lesson_information_1'},
                         {'cmd': 'lesson_information_2'},
                         {'cmd': 'lesson_information_3'},
                         {'cmd': 'lesson_information_4'},
                         {'cmd': 'lesson_information_5'},
                         {'cmd': 'lesson_information_6'},
                         {'cmd': 'lesson_information_7'}])
async def lesson_information(message: Message):
    userInfo = await bp.api.users.get(message.from_id)

    db.edit_account_lesson(userInfo[0].id, message.payload[27::29])
    db.commit()

    day = db.get_account_day(userInfo[0].id)

    diary = await get_diary(
        db.get_account_login(userInfo[0].id),
        db.get_account_password(userInfo[0].id)
    )

    lesson = diary.schedule[day].lessons[int(message.payload[27::29])]

    marks = ''
    homework = ''

    for i in lesson.assignments:
        #Если оценка не равна пустоте, то записываем ее
        if i.mark != None:
            marks += str(i.mark) + ' '

        #Если тип задание = дз, то записываем
        if i.type == 'Домашнее задание':
            homework = i.content
            pass
        else:
            homework = 'не задано'

    #print(lesson.subject)
    #print(lesson.room)
    #print(f'{lesson.start:%H, %M} - {lesson.end:%H.%M}')
    #print(lesson.assignments)
    #print(lesson.assignments[0].content)
    #print(marks)

    await message.answer(f"""
Предмет: {lesson.subject}
Кабинет: {lesson.room}
Время проведения урока: {lesson.start:%H.%M} - {lesson.end:%H.%M}
Домашние задание: {homework}
Оценка: {marks}
    """)
