from typing import Union, List, Text
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

# На что начинается колбэк
class PayloadStarts(ABCRule[Message]):
    def __init__(self, text):
        self.text = text

    async def check(self, event: Message) -> bool:
        payload = event.payload
        if payload is None:
            return False

        if isinstance(self.text, List):
            for i in self.text:
                if payload.startswith(i): return True
            return False

        elif isinstance(self.text, Text):
            return payload.startswith(self.text)