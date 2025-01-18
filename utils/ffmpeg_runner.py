import subprocess
import re
import time
from utils.progress import progress

async def run_ffmpeg_with_progress(command, total_duration, message, update_interval=10):
    """
    Runs FFmpeg with progress updates.
    """
    start_time = time.time()
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
    )

    for line in process.stderr:
        match = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
        if match:
            current_time = parse_ffmpeg_time(match.group(1))
            await progress(current_time, total_duration, start_time, "Converting...", message, update_interval)

    process.wait()
    if process.returncode != 0:
        raise Exception(f"FFmpeg failed: {process.stderr.read()}")

def parse_ffmpeg_time(timestamp):
    """
    Converts FFmpeg timestamp to seconds.
    """
    hours, minutes, seconds = map(float, timestamp.split(":"))
    return hours * 3600 + minutes * 60 + seconds
