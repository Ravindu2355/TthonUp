import aiohttp
import os
from utils.file_utils import get_filename_from_url, generate_unique_filename
from utils.progress import Progress
from utils.ffmpeg_runner import run_ffmpeg_with_progress
from config import bot


async def handle_url(event):
    url = event.message.text.strip()

    # Get filename
    filename = get_filename_from_url(url)
    if not filename:
        filename = generate_unique_filename()
    filepath = f"downloads/{filename}"

    # Download the file
    progress = Progress(bot, event)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            with open(filepath, "wb") as file:
                downloaded = 0
                async for chunk in response.content.iter_chunked(1024 * 1024):
                    file.write(chunk)
                    downloaded += len(chunk)
                    await progress.update_progress(
                        task="Downloading",
                        current=downloaded,
                        total=total_size,
                    )

    # Convert to MP4 if video and not MP4
    if not filename.endswith(".mp4") and "video" in response.headers.get("Content-Type", ""):
        mp4_path = filepath.rsplit(".", 1)[0] + ".mp4"
        filepath = await run_ffmpeg_with_progress(filepath, mp4_path, progress)

    # Upload to Telegram
    thumbnail_path = f"thumbnails/{filename.rsplit('.', 1)[0]}.jpg"
    os.system(f"ffmpeg -i {filepath} -vf thumbnail -frames:v 1 {thumbnail_path}")
    await event.reply("Uploading file...")
    await bot.send_file(
        event.chat_id,
        file=filepath,
        thumb=thumbnail_path,
        caption="Here is your file!",
        supports_streaming=True,
    )

    # Clean up
    os.remove(filepath)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
