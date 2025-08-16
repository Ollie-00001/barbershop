import os
import asyncio
from django.conf import settings
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', os.getenv('TELEGRAM_BOT_TOKEN'))
TELEGRAM_CHAT_ID = getattr(settings, 'TELEGRAM_CHAT_ID', os.getenv('TELEGRAM_CHAT_ID'))

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    async def _send():
        try:
            print("Sending telegram message:", text)
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode='Markdown')
        except Exception as e:
            print("Error sending telegram message:", e)

    asyncio.run(_send())