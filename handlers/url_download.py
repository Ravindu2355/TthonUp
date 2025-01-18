import aiohttp
import os
import time
from utils.progress import progress

async def download_url(url, file_path, message):
    """
    Download a file from a URL with progress updates.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.edit(f"Failed to download. HTTP Status: {response.status}")
                return

            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            with open(file_path, "wb") as file:
                async for chunk in response.content.iter_chunked(1024 * 1024):  # 1MB chunks
                    file.write(chunk)
                    downloaded += len(chunk)
                    await progress(downloaded, total, start_time, "Downloading...", message)
