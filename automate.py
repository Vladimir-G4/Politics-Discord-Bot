from DiscordBot import autoUpdate
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.get_event_loop().run_until_complete(autoUpdate())
