from vkbottle.bot import Message, Blueprint
from PostgreSQLighter import db
from vkbottle import CtxStorage, BaseStateGroup
import logging
import asyncio
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from ns import get_school
import traceback
from commands.menu import private_menu



bp = Blueprint('schedule_download') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


ctx = CtxStorage() # объявляем временное хранилище

#Нужно, для запоминания где сейчас юзер
class ScheduleData(BaseStateGroup):
    PHOTO = 1
    SCHOOL = 2
    CLAS = 3
    SCHOOL2 = 4
    SCHOOL3 = 5
    FINISH = 6

@bp.on.chat_message(payload={'cmd': 'schedule_download'})
@bp.on.chat_message(text=['/загрузить расписание', '/загрузить расп', '/лоадрасп', '/loadshedule'])
async def start_schedule_download(message: Message):
    await message.answer("Доступно только в л/с!")

@bp.on.message(payload={'cmd': 'schedule_download'})
@bp.on.private_message(text=['/загрузить расписание', '/загрузить расп', '/лоадрасп', '/loadshedule'])
async def start_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get /loadshedule')

    keyboard = (
        Keyboard()
        .add(Text('Понедельник'))
        .row()
        .add(Text('Вторник'))
        .row()
        .add(Text('Среда'))
        .row()
        .add(Text('Четверг'))
        .row()
        .add(Text('Пятница'))
        .row()
        .add(Text('Суббота'))
        .row()
        .add(Text('Назад', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await bp.state_dispenser.set(message.peer_id, ScheduleData.PHOTO) # Говорим, что следующий шаг - выбор фото
    await message.answer("На какой день хочешь загрузить расписание?", keyboard=keyboard)


@bp.on.private_message(state=ScheduleData.PHOTO)
async def photo_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get day in schedule_download')
    ctx.set('day', message.text) # Загружаем во внутренне хранилище день недели
    await bp.state_dispenser.set(message.peer_id, ScheduleData.SCHOOL) # Говорим, что следующий шаг - выбор школы
    await message.answer("Отправь фото расписания", keyboard=EMPTY_KEYBOARD)


@bp.on.private_message(state=ScheduleData.SCHOOL)
async def school_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get photo in schedule_download')
    photo = message.attachments[0].photo
    ctx.set('photo', f'photo{photo.owner_id}_{photo.id}_{photo.access_key}') # Загружаем во внутренне хранилище фото
    await bp.state_dispenser.set(message.peer_id, ScheduleData.SCHOOL2) # Говорим, что следующий шаг - выбор школы
    
    keyboard = (
        Keyboard()
        .add(Text('Да, для моей', {'LoadShedule': 'itsmyschool'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Нет, для другой', {'LoadShedule': 'itsnotmyschool'}), color=KeyboardButtonColor.SECONDARY)
    )

    await message.answer("Это расписание для твоей школы?", keyboard=keyboard)

@bp.on.private_message(state=ScheduleData.SCHOOL2, payload={'LoadShedule': 'itsmyschool'})
async def itsmyschool_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get itsmyschool in schedule_download')
    await message.answer('Хорошо, так и запишу')
    await bp.state_dispenser.set(message.peer_id, ScheduleData.CLAS)
    await class_schedule_download(message)

@bp.on.private_message(state=ScheduleData.SCHOOL2, payload={'LoadShedule': 'itsnotmyschool'})
async def itsnotmyschool_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get itsnotmyschool in schedule_download')
    await message.answer('🖊Введите адрес сетевого города (Пример: "https://sgo.edu-74.ru/").', keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, ScheduleData.SCHOOL3)


@bp.on.private_message(state=ScheduleData.SCHOOL3)
async def itsnotmyschool2_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get itsnotmyschool2 in schedule_download')
    if message.attachments:
        if message.attachments[0].link:
            link = 'https://' + str(message.attachments[0].link.caption) + '/'

    if message.text or link:
        try:
            if message.text:
                link = message.text

            ctx.set('link', link) # Загружаем во временное хранилище ссылку

            schools = await get_school(link)
            await message.answer('📋Введи ID школы из списка ниже(ID - Школа)')
            await asyncio.sleep(2)
            text = ''
            for school in schools:
                text += f"\n{school['id']} - {school['name']}"
            if len(text) > 4096:
                for x in range(0, len(text), 4096):
                    await message.answer(text[x:x+4096])
                    await asyncio.sleep(1,5)
                await message.answer('✅Всё!')
            else:
                await message.answer(text)
            await bp.state_dispenser.set(message.peer_id, ScheduleData.CLAS)
        except Exception as e:
            print(traceback.print_exc())
            await message.answer(f'❌Ошибка: {e}\nПопробуйте еще раз или обратитесь к [kirillarz|разработчику]')
    else:
        await message.answer('❌Не нашел в твоем сообщении данные, введи еще раз')


    
@bp.on.private_message(state=ScheduleData.CLAS)
async def class_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get itsmyschool in schedule_download')
    userId = message.from_id # ID юзера

    if message.payload is None:
        link = ctx.get('link')
        school = message.text

        for i in await get_school(link):
            if i['id'] == int(school):
                school = i['name']
                break

        ctx.set('school', school) 
        await bp.state_dispenser.set(message.peer_id, ScheduleData.FINISH) 

    else:
        ctx.set('school', db.get_account_school(userId))
        await bp.state_dispenser.set(message.peer_id, ScheduleData.FINISH)

    keyboard = (
        Keyboard()
        .add(Text('Это расписание для всей школы', {'LoadShedule': 'ItsSheduleForAllSchool'}), color=KeyboardButtonColor.SECONDARY)
    )

    await message.answer("Теперь отправь класс, на который загружаешь расписание", keyboard=keyboard)


@bp.on.private_message(state=ScheduleData.FINISH)
async def finish_schedule_download(message: Message):
    logging.info(f'{message.peer_id}: I get finish in schedule_download')

    day = ctx.get('day')
    photo = ctx.get('photo')
    school = ctx.get('school')

    if message.text == 'Это расписание для всей школы':
        for i in set(db.get_account_any_with_filter('class', 'school', school)):
            clas = i[0]
            try:
                old_shedule = db.get_schedule(school, clas, day)
                db.edit_schedule(school, clas, day, photo)
            except:
                db.add_schedule(school, clas, day, photo)
        clas = 'all'

    else: 
        clas = message.text.lower()

        try:
            old_shedule = db.get_schedule(school, clas, day)
            db.edit_schedule(school, clas, day, photo)
        except:
            db.add_schedule(school, clas, day, photo)

    users_with_notification = db.get_accounts_schedule_notification()
    chats_with_notification = db.get_chats_schedule_notification()
    for i in users_with_notification:
        i_id = i[0]
        if db.get_account_school(i_id) == school:
            if db.get_account_class(i_id) == clas or clas == 'all':
                await bp.api.messages.send(message='Новое расписание!', user_id=i_id, random_id=0, attachment=photo)
                await asyncio.sleep(1)

    for i in chats_with_notification:
        i_id = i[0]
        if db.get_chat_school(i_id) == school:
            if db.get_chat_class(i_id) == clas or clas == 'all':
                await bp.api.messages.send(message='Новое расписание!', peer_id=2000000000+i_id, random_id=0, attachment=photo)
                await asyncio.sleep(1)

    await message.answer('Расписание успешно обновлено!', attachment=photo)
    await bp.state_dispenser.delete(message.from_id)
    logging.info(f'{message.peer_id}: I sent success')

    await private_menu(message)