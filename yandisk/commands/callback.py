from yandisk import client, Yandex
from telethon.events import CallbackQuery
from re import compile
from telethon.tl.custom import Button
from os import remove

@client.on(CallbackQuery)
async def callquery(event):
    data = event.data.decode("utf-8")
    
    if data.startswith("nodelete"):
        filename = data.split("nodelete-")[1]
        await Yandex.publish(filename)
        file = await Yandex.get_meta(filename)
        await event.edit(f"**Here is the link of the old file: ** [Link]({file.public_url})", buttons=Button.url('🔗 Public Link', file.public_url))
    elif data.startswith("remove"):
        filename = data.split("remove-")[1]
        await event.edit(f"**Are you sure for delete `{filename}` permanently?**", buttons=[Button.inline('✅ Yes', f"yes-{filename}"), Button.inline('❌ No', "no")])
    elif data.startswith("yes"):
        filename = data.split("yes-")[1]
        await Yandex.remove(filename, permanently=True)
        return await event.edit(f"✅ **Deleted successfully!**")
    elif data == "no":
        return await event.edit("__OK! File will not be deleted.__")
    elif data.startswith("publish"):
        filename = data.split("publish-")[1]
        await Yandex.publish(filename)
        file = await Yandex.get_meta(filename)
        await event.edit(f"__✅ I made the file public.__ **Here is public link: ** [Link]({file.public_url})", buttons=Button.url('🔗 Public Link', file.public_url))
        
        return remove(file)
    elif data == "nopublish":
        return await event.edit("__OK! Only you will access the file.__")