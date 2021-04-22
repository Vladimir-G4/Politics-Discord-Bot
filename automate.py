from DiscordBot import autoUpdate
import time
import asyncio

time.sleep(4)
asyncio.set_event_loop(asyncio.ProactorEventLoop())
asyncio.get_event_loop().run_until_complete(autoUpdate())
