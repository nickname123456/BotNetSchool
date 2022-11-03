from vkbottle import Bot, PhotoMessageUploader

async def send_vk_msg(bot: Bot, message: str, user_id: int = None, chat_id: int = None):
    if user_id:
        await bot.api.messages.send(message=message, user_id=user_id, random_id=0)
    elif chat_id:
        await bot.api.messages.send(message=message, peer_id=2000000000+chat_id, random_id=0)

async def send_vk_bytes_photo(bot: Bot, photo: bytes, user_id: int = None, chat_id: int = None, caption: str = None):
    photo = await PhotoMessageUploader(api=bot.api).upload(photo)

    if user_id:
        await bot.api.messages.send(message=caption, attachment=photo, user_id=user_id, random_id=0)
    elif chat_id:
        await bot.api.messages.send(message=caption, attachment=photo, peer_id=2000000000+chat_id, random_id=0)