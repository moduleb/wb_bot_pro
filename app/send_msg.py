from app.bot import bot


async def send_msg(user_id, msg):
    await bot.send_message(chat_id=user_id, text=msg)