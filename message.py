import telegram

import config


async def send_message(text):
    bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
    chat_id = config.TELEGRAM_CHAT_ID
    async with bot:
        await bot.sendMessage(chat_id=chat_id, text=text)
