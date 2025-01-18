import time


class Progress:
    def __init__(self, bot, event):
        self.bot = bot
        self.event = event
        self.last_update = time.time()

    async def update_progress(self, task, current, total):
        now = time.time()
        if now - self.last_update < 10:  # Update every 10 seconds
            return

        percentage = (current / total) * 100 if total > 0 else 0
        message = (
            f"{task}...\n"
            f"Completed: {current / 1024 / 1024:.2f} MB of {total / 1024 / 1024:.2f} MB\n"
            f"Progress: {percentage:.2f}%"
        )
        await self.event.edit(message)
        self.last_update = now
