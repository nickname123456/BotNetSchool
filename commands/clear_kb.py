from vkbottle.bot import Message, Blueprint
from vkbottle import EMPTY_KEYBOARD
import logging


bp = Blueprint('clear_kb') # Объявляем команду
bp.on.vbml_ignore_case = True# Игнорируем регистр


@bp.on.message(text=['убери', 'спрячь', '/убери', '/спрячь', '/клавиатура',
                    'e,thb', 'cghzxm', '/e,thb', '/cghzxm', '/rkfdbfnehf'])
async def clear_kb(message: Message):
    logging.info(f'{message.peer_id}: I get clear_bp')

    await message.answer('Клавиатура спрятана!', keyboard=EMPTY_KEYBOARD)