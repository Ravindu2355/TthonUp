import time

last_update_time = 0  # Tracks last update time for messages

async def progress(current, total, start_time, msg, message, update_interval=10):
    """
    Updates Telegram progress messages.
    """
    global last_update_time
    now = time.time()

    if now - last_update_time >= update_interval or current == total:
        percent = (current / total) * 100
        elapsed_time = now - start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0
        eta = (total - current) / speed if speed > 0 else 0

        text = (
            f"{msg}\n"
            f"Progress: [{'#' * int(percent // 10)}{'-' * (10 - int(percent // 10))}] {percent:.2f}%\n"
            f"Transferred: {current / 1024**2:.2f}MB/{total / 1024**2:.2f}MB\n"
            f"Speed: {speed / 1024**2:.2f} MB/s\n"
            f"ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}\n"
            f"Elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
        )

        await message.edit(text)
        last_update_time = now
