from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

# На что начинается колбэк
class PayloadStarts(ABCRule[Message]):
    def __init__(self, text):
        self.text = text

    async def check(self, event: Message) -> bool:
        payload = event.payload
        return payload.startswith(self.text)