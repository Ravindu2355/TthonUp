from telethon import events
from config import bot
from utils.ffmpeg_runner import run_ffmpeg_with_progress
from utils.progress import progress
from moviepy.editor import VideoFileClip
import os
import time

THUMBNAIL_DIR = "thumbnails/"
CONVERTED_DIR = "converted/"
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)

@bot.on(events.NewMessage(pattern="/upload"))
async def upload_file(event):
    if not event.file:
        await event.reply("Please attach a video file to upload.")
        return

    file_name = event.message.file.name
    file_path = f"downloads/{file_name}"
    os.makedirs("downloads", exist_ok=True)
    start_time = time.time()

    # Download the file
    msg = await event.reply("Starting download...")
    await bot.download_media(
        event.message,
        file_path,
        progress_callback=lambda current, total: progress(current, total, start_time, "Downloading...", msg),
    )

    # Check if the file is a video and convert if necessary
    converted_path = (
        await convert_to_mp4(file_path, msg) if not file_name.endswith(".mp4") else file_path
    )

    # Generate thumbnail
    try:
        thumbnail_path = generate_thumbnail(converted_path)
    except Exception as e:
        await event.reply(f"Error generating thumbnail: {str(e)}")
        return

    # Upload the file
    try:
        start_time = time.time()
        await bot.send_file(
            event.chat_id,
            file=converted_path,
            caption="Streamable video with progress",
            supports_streaming=True,
            thumb=thumbnail_path,
            progress_callback=lambda current, total: progress(current, total, start_time, "Uploading...", msg),
        )
        await msg.edit("Video uploaded successfully!")
    except Exception as e:
        await msg.edit(f"Error uploading video: {str(e)}")

    # Cleanup
    os.remove(file_path)
    os.remove(thumbnail_path)
    if file_path != converted_path:
        os.remove(converted_path)

async def convert_to_mp4(input_path, msg):
    """
    Convert the video file to MP4 using FFmpeg.
    """
    output_path = os.path.join(CONVERTED_DIR, os.path.basename(input_path).rsplit(".", 1)[0] + ".mp4")
    clip = VideoFileClip(input_path)
    total_duration = clip.duration
    clip.close()

    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path,
    ]

    await run_ffmpeg_with_progress(command, total_duration, msg)
    return output_path

def generate_thumbnail(video_path):
    """
    Generate a thumbnail from the first frame of the video using moviepy.
    """
    clip = VideoFileClip(video_path)
    thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{os.path.basename(video_path)}.jpg")
    clip.save_frame(thumbnail_path, t=0)
    clip.close()
    return thumbnail_path
