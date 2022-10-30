from aiogram import Bot

async def send_telegram_msg(bot: Bot, chat_id: int, message: str):
    await bot.send_message(chat_id=chat_id, text=message)