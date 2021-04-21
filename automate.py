from DiscordBot import autoUpdate
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(autoUpdate())
loop.run_until_complete(asyncio.sleep(1))
loop.close()
