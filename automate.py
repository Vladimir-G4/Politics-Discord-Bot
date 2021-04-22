from DiscordBot import autoUpdate
import time
import asyncio

time.sleep(3)
loop = asyncio.new_event_loop()
loop.run_until_complete(autoUpdate())
