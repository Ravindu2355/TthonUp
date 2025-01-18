import time


class Progress:
    def __init__(self, bot, event):
        self.bot = bot
        self.event = event
        self.progress_message = None  # The message for progress updates
        self.last_update = time.time()
        self.last_message = ""  # Store the last message content

    async def create_progress_message(self, task):
        """Send a new message for progress updates."""
        self.progress_message = await self.event.reply(f"{task}...")

    async def update_progress(self, task, current, total):
        """Update the progress message."""
        now = time.time()
        if now - self.last_update < 10:  # Update every 10 seconds
            return

        percentage = (current / total) * 100 if total > 0 else 0
        message = (
            f"{task}...\n"
            f"Completed: {current / 1024 / 1024:.2f} MB of {total / 1024 / 1024:.2f} MB\n"
            f"Progress: {percentage:.2f}%"
        )

        # Avoid sending the same message again
        if message == self.last_message:
            return

        if self.progress_message:
            try:
                await self.progress_message.edit(message)
                self.last_message = message  # Update the last sent message
            except:
                # Handle the case where the message is no longer editable
                pass

        self.last_update = now
