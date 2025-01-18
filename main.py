from telethon import events
from config import bot
from handlers.url_handler import handle_url
from handlers.telegram_handler import handle_telegram_upload
import os

os.makedirs("downloads", exist_ok=True)

@bot.on(events.NewMessage(pattern="/upload"))
async def upload_handler(event):
    await handle_telegram_upload(event)


@bot.on(events.NewMessage())
async def url_handler(event):
    if event.message.text.startswith("http"):
        await handle_url(event)


print("Bot is running...")
bot.run_until_disconnected()
