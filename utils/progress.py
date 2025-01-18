import time

class Progress:
    def __init__(self, event, initial_message):
        self.event = event
        self.message = None
        self.last_update = 0
        self.text = initial_message

    async def update(self, text):
        self.text = text
        if time.time() - self.last_update > 10:
            if self.message:
                await self.message.edit(text)
            else:
                self.message = await self.event.reply(text)
            self.last_update = time.time()

    async def done(self, text):
        if self.message:
            await self.message.edit(text)
