from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging



bp = Blueprint('admin_panel')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Вход" или нажали на соответствующую кнопку
@bp.on.message(text=["Найти <userId>"])
async def login(message: Message, userId=None):
    pass
