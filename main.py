from telethon import events
from config import bot
from handlers.upload import upload_file
from handlers.url_download import download_url
import os

# Ensure necessary directories exist
os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)
os.makedirs("converted", exist_ok=True)

# Start bot
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Hello! I'm your URL Uploader bot. Use /upload to upload videos or /download to download files from URLs.")

# Register handlers
bot.add_event_handler(upload_file)
bot.add_event_handler(download_url)

# Run the bot
print("Bot is running...")
bot.run_until_disconnected()
