from DiscordBot import autoUpdate
import asyncio

asyncio.get_event_loop().run_until_complete(autoUpdate())
