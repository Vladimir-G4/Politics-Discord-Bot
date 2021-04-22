from DiscordBot import autoUpdate
import time
import asyncio

time.sleep(4)
loop = asyncio.new_event_loop()
loop.run_until_complete(autoUpdate())
