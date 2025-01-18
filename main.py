import os
from config import bot
from handlers.url_handler import handle_url
from handlers.reply_handler import handle_reply
from telethon import events

# Ensure necessary directories exist
os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)
os.makedirs("converted", exist_ok=True)

# Handle messages containing URLs
@bot.on(events.NewMessage(pattern=r"https?://"))
async def url_event_handler(event):
    await handle_url(event)

# Handle replies with /upload
@bot.on(events.NewMessage(pattern="/upload"))
async def reply_event_handler(event):
    await handle_reply(event)

# Start the bot
print("Bot is running...")
bot.run_until_disconnected()
