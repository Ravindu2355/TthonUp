import os
from utils.progress import Progress
from utils.ffmpeg_runner import run_ffmpeg_with_progress
from config import bot


async def handle_telegram_upload(event):
    if not event.message.is_reply:
        await event.reply("Reply to a video with `/upload`.")
        return

    reply_message = await event.get_reply_message()
    if not reply_message.video:
        await event.reply("The replied message must contain a video.")
        return

    progress = Progress(bot, event)
    video = reply_message.video
    filepath = f"downloads/{video.file_name}"

    # Download the video
    await bot.download_media(reply_message, file=filepath)
    await progress.update_progress("Downloading", 1, 1)

    # Convert to MP4 if not already MP4
    if not filepath.endswith(".mp4"):
        mp4_path = filepath.rsplit(".", 1)[0] + ".mp4"
        filepath = await run_ffmpeg_with_progress(filepath, mp4_path, progress)

    # Upload to Telegram
    thumbnail_path = f"thumbnails/{video.file_name.rsplit('.', 1)[0]}.jpg"
    os.system(f"ffmpeg -i {filepath} -vf thumbnail -frames:v 1 {thumbnail_path}")
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
