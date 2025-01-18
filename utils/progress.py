import time


class Progress:
    def __init__(self, bot, event):
        self.bot = bot
        self.event = event
        self.progress_message = None  # The message for progress updates
        self.last_update = time.time()
        self.last_message = ""  # Store the last message content
        self.start_time = None  # Time when progress starts

    async def create_progress_message(self, task):
        """Send a new message for progress updates."""
        self.start_time = time.time()  # Mark the start time
        self.progress_message = await self.event.reply(f"{task}...")

    async def update_progress(self, task, current, total, speed=None, eta=None):
        """Update the progress message."""
        now = time.time()
        if now - self.last_update < 10:  # Update every 10 seconds
            return

        # Calculate speed and ETA if not provided
        elapsed_time = now - self.start_time if self.start_time else 0
        if speed is None:
            speed = current / elapsed_time if elapsed_time > 0 else 0
        if eta is None and speed > 0:
            eta = (total - current) / speed

        # Prepare progress message
        percentage = (current / total) * 100 if total > 0 else 0
        message = (
            f"{task}...\n"
            f"Completed: {current / 1024 / 1024:.2f} MB of {total / 1024 / 1024:.2f} MB\n"
            f"Progress: {percentage:.2f}%\n"
            f"Speed: {speed / 1024 / 1024:.2f} MB/s\n"
            f"ETA: {int(eta)} seconds"
        )

        # Avoid sending the same message again
        if message == self.last_message:
            return

        # Update the progress message
        if self.progress_message:
            try:
                await self.progress_message.edit(message)
                self.last_message = message  # Update the last sent message
            except:
                # Handle the case where the message is no longer editable
                pass

        self.last_update = now

    async def complete(self, message="Task completed!"):
        """Mark progress as complete and update the message."""
        if self.progress_message:
            try:
                await self.progress_message.edit(message)
            except:
                # Handle case where the message cannot be edited
                pass
