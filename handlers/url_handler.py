import aiohttp
import os
import time
from utils.file_utils import get_filename_from_url, generate_unique_filename
from utils.progress import Progress
from utils.ffmpeg_runner import run_ffmpeg_with_progress
from config import bot
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata


async def handle_url(event):
    url = event.message.text.strip()

    # Ensure downloads directory exists
    os.makedirs("downloads", exist_ok=True)

    # Get filename
    filename = get_filename_from_url(url)
    if not filename:
        filename = generate_unique_filename()
    filepath = f"downloads/{filename}"

    # Create progress handler
    progress = Progress(bot, event)
    await progress.create_progress_message("Starting download")

    # Download the file
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            with open(filepath, "wb") as file:
                downloaded = 0
                start_time = time.time()
                async for chunk in response.content.iter_chunked(1024 * 1024):
                    file.write(chunk)
                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time
                    speed = downloaded / elapsed_time if elapsed_time > 0 else 0
                    eta = (total_size - downloaded) / speed if speed > 0 else 0
                    await progress.update_progress(
                        task="Downloading",
                        current=downloaded,
                        total=total_size,
                        speed=speed,
                        eta=eta,
                    )

    # Convert to MP4 if video and not MP4
    if not filename.endswith(".mp4") and "video" in response.headers.get("Content-Type", ""):
        mp4_path = filepath.rsplit(".", 1)[0] + ".mp4"
        filepath = await run_ffmpeg_with_progress(filepath, mp4_path, progress)

    # Upload to Telegram
    thumbnail_path = f"thumbnails/{filename.rsplit('.', 1)[0]}.jpg"
    os.makedirs("thumbnails", exist_ok=True)
    os.system(f"ffmpeg -i {filepath} -vf thumbnail -frames:v 1 {thumbnail_path}")

    # Upload with progress
    async def upload_progress(current, total):
        elapsed_time = time.time() - start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0
        eta = (total - current) / speed if speed > 0 else 0
        percentage = (current / total) * 100 if total > 0 else 0
        await progress.update_progress(
            task="Uploading",
            current=current,
            total=total,
            speed=speed,
            eta=eta,
        )

    start_time = time.time()
    '''
    with open(filepath, "rb") as file:
       await bot.send_file(
          event.chat_id,
          file=file,
          thumb=thumbnail_path,
          caption="Here is your file!",
          supports_streaming=True,
          progress_callback=upload_progress,
          part_size_kb=1024
       )
    '''
    edit = await bot.send_message(event.chat_id, "Trying to process.")
    out2=filepath
    text = filepath
    metadata = video_metadata(out2)
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration"]
    attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
    try:
        uploader = await fast_upload(f'{out2}', f'{out2}', start_time, bot, edit, '**UPLOADING:**')
        await bot.send_file(event.chat_id, uploader, caption=text, attributes=attributes, force_document=False)
    except Exception:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', start_time, bot, edit, '**UPLOADING:**')
            await bot.send_file(event.chat_id, uploader, caption=text, force_document=True)
        except Exception as e:
            await edit.edit(f"failed:  {e}")
    # Clean up
    os.remove(filepath)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    await progress.progress_message.edit("Task completed!")
