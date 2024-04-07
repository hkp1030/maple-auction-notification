import telegram

import config

BOT = telegram.Bot(token=config.TELEGRAM_TOKEN)


async def get_chat_id():
    updates = await BOT.getUpdates()
    chat_id = updates[-1].message.chat.id
    return chat_id


async def send_message(text):
    chat_id = await get_chat_id()
    await BOT.sendMessage(chat_id=chat_id, text=text)
