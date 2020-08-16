from . import client
from .commands import ALL_COMMANDS
import asyncio
import importlib
from logging import getLogger, basicConfig, INFO
from os import environ

basicConfig(
    format="%(asctime)s | %(name)s - [%(levelname)s] --> %(message)s",
    level=INFO)

loop = asyncio.get_event_loop()
async def main():    
    await client.start(bot_token=environ.get("BOT_TOKEN"))
    for command in ALL_COMMANDS:
        importlib.import_module("yandisk.commands." + command)

loop.run_until_complete(main())
loop.run_forever()
