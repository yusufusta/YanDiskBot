from yandisk import token, Yandex
from yandisk.events import message
from yadisk_async.exceptions import BadRequestError
from telethon.events import NewMessage
from telethon.tl.custom import Button

@message(incoming=True, pattern="/login")
async def login(event):
    global token
    if token is not None:
        return await event.edit("`You are already logged!`")

    async with event.client.conversation(event.chat_id) as conv:
        url = Yandex.get_code_url()
        await conv.send_message(f"To login;\nFirst go to [this link]({url}), then allow the app. It will give you a number, write it.", buttons=Button.url('🔗 Link', url))
        response = await conv.wait_event(NewMessage(incoming=True,from_users=event.chat_id))

        try:
            token2 = await Yandex.get_token(response.message.raw_text)
        except BadRequestError:
            return await event.reply("**You entered an invalid code! Token process canceled.**")

        Yandex.token = token2.access_token
        if await Yandex.check_token():
            token = Yandex.token
            open("token.txt", "a+").write(token)
            await event.reply("**✅ Your token has been successfully added. Now you can use this bot.**")
        else:
            await event.reply("**❌ Something went wrong. Not sure how though...**")
