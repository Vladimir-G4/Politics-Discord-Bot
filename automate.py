from DiscordBot import autoUpdate
import time
import asyncio

time.sleep(3)
loop = asyncio.new_event_loop()
loop.call_soon(autoUpdate())
