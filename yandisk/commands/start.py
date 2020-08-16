from yandisk.events import message

@message(pattern="/start")
async def start(event):
    await event.reply(
        f"""
**Working!**
"""
    )