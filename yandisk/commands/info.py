from yandisk import humanbytes, Yandex
from yandisk.events import message

@message(pattern="/info")
async def info(event):
    info = await Yandex.get_disk_info()
    await event.reply(
        f"""
**Successfully logged as `{info.user.login}`!**

**Disk Used Space: **`{humanbytes(info.used_space)}`
**Disk Total Space: **`{humanbytes(info.total_space)}`
"""
    )