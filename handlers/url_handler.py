import os
import aiohttp
from telethon.tl.types import DocumentAttributeVideo
from utils.progress import Progress
from utils.ffmpeg_runner import run_ffmpeg
from utils.thumbnail_generator import generate_thumbnail

async def handle_url(event):
    url = event.text.strip()
    progress = Progress(event, "Downloading file from URL...")

    # Download file
    file_name = os.path.basename(url) or f"file_{event.id}"
    file_path = f"downloads/{file_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(file_path, "wb") as f:
                    f.write(await resp.read())
            else:
                await event.reply("Failed to download the file.")
                return

    await progress.update("File downloaded. Checking file type...")

    # Convert to MP4 if needed
    converted_path = file_path
    if not file_path.endswith(".mp4"):
        converted_path = f"converted/{file_name}.mp4"
        await run_ffmpeg(file_path, converted_path, progress)

    # Generate thumbnail
    thumbnail_path = f"thumbnails/{file_name}.jpg"
    generate_thumbnail(converted_path, thumbnail_path)

    # Upload file
    await progress.update("Uploading the video to Telegram...")
    await event.client.send_file(
        event.chat_id,
        converted_path,
        thumb=thumbnail_path,
        supports_streaming=True,
        attributes=[
            DocumentAttributeVideo(duration=0, w=0, h=0, supports_streaming=True)
        ],
    )
    await progress.done("Upload complete.")

    # Cleanup
    os.remove(file_path)
    os.remove(converted_path)
    os.remove(thumbnail_path)
