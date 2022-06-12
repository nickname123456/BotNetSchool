from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text
import logging


bp = Blueprint('reports') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений



@bp.on.message(payload={'cmd': 'reports'})
@bp.on.message(text = 'отчеты')
async def reports(message: Message):
    logging.info(f'{message.peer_id}: I get reports')

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