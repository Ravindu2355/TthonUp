import os
from utils.progress import Progress
from utils.ffmpeg_runner import run_ffmpeg
from utils.thumbnail_generator import generate_thumbnail
from telethon.tl.types import DocumentAttributeVideo

async def handle_reply(event):
    if not event.is_reply:
        await event.reply("Please reply to a video message with /upload.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg.video:
        await event.reply("This command only works on video messages.")
        return

    progress = Progress(event, "Downloading the video from Telegram...")

    # Download video
    file_name = f"replied_{event.id}.mp4"
    file_path = f"downloads/{file_name}"
    await reply_msg.download_media(file_path)
    await progress.update("Video downloaded. Converting if necessary...")

    # Convert to MP4 if needed
    converted_path = file_path
    if not file_path.endswith(".mp4"):
        converted_path = f"converted/{file_name}"
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
