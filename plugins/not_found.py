from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink
from vkbottle.bot import Blueprint


bp = Blueprint('not_found')
bp.on.vbml_ignore_case = True


#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.message(payload={'cmd': 'not_found'})
async def not_found(message: Message):
    keyboard = (
        Keyboard()
        .add(OpenLink('https://vk.com/im?sel=457641188', 'Администратор'), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад", {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('Если возникли проблемы обратитесь к Администратору', keyboard=keyboard)
