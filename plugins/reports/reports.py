from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging


bp = Blueprint('reports') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.private_message(payload={'cmd': 'reports'})
@bp.on.private_message(text = 'отчеты')
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get reports')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Итоговые отметки', {'cmd': 'reportTotal'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Средний балл', {'cmd': 'reportAverageMark'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Информационное письмо для родителей', {'cmd': 'parentReport'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    
    logging.info(f'{message.peer_id}: I sent reports')
    await message.answer('Вот доступные отчеты:', keyboard=keyboard)


@bp.on.chat_message(payload={'cmd': 'reports'})
@bp.on.chat_message(text = 'отчеты')
async def marks(message: Message):
    logging.info(f'{message.peer_id}: I get reports')
    # Айди чата:
    chat_id = message.chat_id

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Итоговые отметки', {'cmd': 'reportTotal'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Средний балл', {'cmd': 'reportAverageMark'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Информационное письмо для родителей', {'cmd': 'parentReport'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    
    logging.info(f'{message.peer_id}: I sent reports')
    await message.answer('Вот доступные отчеты:', keyboard=keyboard)