import subprocess


async def run_ffmpeg_with_progress(input_path, output_path, progress):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        output_path,
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        await progress.update_progress("Converting with FFmpeg", 1, 1)
    return output_path
