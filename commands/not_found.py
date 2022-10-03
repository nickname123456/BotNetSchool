from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink
import logging


bp = Blueprint('not_found') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


@bp.on.message(text=['/report', '/htgjhn', '/репорт'])
@bp.on.message(payload={'cmd': 'not_found'})
async def not_found(message: Message):
    logging.info(f'{message.peer_id}: I get not_found')
    keyboard = (
        Keyboard()
        .add(OpenLink('https://vk.com/im?sel=457641188', 'Администратор'), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('Если возникли проблемы обратитесь к Администратору', keyboard=keyboard)
