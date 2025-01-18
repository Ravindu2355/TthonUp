from telethon import TelegramClient
import os

# Telegram API credentials
API_ID = os.getenv("apiid")
API_HASH = os.getenv("apihash")
BOT_TOKEN = os.getenv("tk")

# Initialize the bot
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
