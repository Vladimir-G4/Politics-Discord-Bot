from DiscordBot import autoUpdate
import time
import asyncio

time.sleep(4)
asyncio.get_event_loop().run_until_complete(autoUpdate())
