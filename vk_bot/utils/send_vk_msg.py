from vkbottle import Bot

async def send_vk_msg(bot: Bot, message: str, user_id: int = None, chat_id: int = None):
    if user_id:
        await bot.api.messages.send(message=message, user_id=user_id, random_id=0)
    elif chat_id:
        await bot.api.messages.send(message=message, peer_id=2000000000+chat_id, random_id=0)