import sys
import os
import yadisk
import sys
import time
import logging
import asyncio

# Import somethings
from config import BOTTOKEN, ADMINID, ADMINUSERNAME, YANDEXAPPID, YANDEXAPPSECRET, APIID, APIHASH
from os.path import join, dirname
from telethon import TelegramClient, events
from telethon import events
from telethon.tl.custom import Button
from hurry.filesize import size, si

session = "yandisk"
api_id = APIID
api_hash = APIHASH
bot_token = BOTTOKEN
debug_enabled = "true"
user_id = ADMINID
admin = ADMINUSERNAME

yandex_app_id = YANDEXAPPID
yandex_app_secret = YANDEXAPPSECRET
client = TelegramClient(session, api_id, api_hash)
logging.basicConfig(level=logging.WARNING)


@client.on(events.CallbackQuery)
async def callback(event):
    if format(event.data) == "b'delete'":
        await event.edit("veri")

@events.register(events.NewMessage)
async def handler(update):
    if update.message.media is not None:
        userid = update.message.from_id

        if str(userid) == user_id:

            if os.path.isfile(str(userid)):
                tokenfile = open(str(userid),'r')
                token2 = tokenfile.read()
                start = time.time()
                message = await update.reply('Download process is starting...')
                async def progress(current, total):
                    sonuc = (current / total) * 100
                    await message.edit("Status: %" + str(round(sonuc,2)) + " Downloaded.\nTotal Size: " + str(size(total, system=si)) + "\nDownloaded Sizze: " + str(size(current, system=si)))
                dosyaismi = await client.download_media(update.message,progress_callback=progress)
                await message.delete()
                message2 = await update.reply("Succesfully downloaded... Uploadinh to Yandex...")
                y = yadisk.YaDisk(token=token2)
                y.upload(dosyaismi, dosyaismi)
                y.publish(dosyaismi)
                await message2.edit("Succesfully uploaded! Getting public-link...")
                link = y.get_meta(dosyaismi).public_url
                finish = time.time() - start
                await message2.delete()
                await client.send_message(userid, "File is uploaded in " + str(round(finish)) + " seconds!", buttons=[
                [Button.url('Public Link', link)]
                ])
                os.unlink(dosyaismi)
            else:
                y = yadisk.YaDisk(yandex_app_id, yandex_app_secret)
                url2 = y.get_code_url()
                async with client.conversation(userid) as conv:
                    try:
                        await conv.send_message('Aşağıdaki butona tıklayıp yandexin websitesine gideceksiniz, ardından uygulamaya izin veriniz, izin verdikten sonra bir kod alacaksınız. O kodu yazınız.', buttons=[
                        [Button.url('Bu uygulamaya izin ver', url2)]
                        ])
                        code = await conv.get_response()
                    except asyncio.TimeoutError as e:
                        await conv.send_message("Timeout error. Please resend media and try again.")
                    try:
                        response = y.get_token(code.raw_text)
                    except yadisk.exceptions.BadRequestError:
                        await conv.send_message("Bad code. Please resend media and try again.")
                        
                    except yadisk.exceptions.ForbiddenError:
                        await conv.send_message("Please, First create YandexDisk user with this link. https://disk.yandex.com/client/disk")
                        
                    if update.message.out == "false":
                        while not any(x.isdigit() for x in code.raw_text):
                            await conv.send_message("Your name didn't have any number! Try again")
                y.token = response.access_token
                if await y.check_token():
                    await conv.send_message("Token başarılı bir şekilde kaydedildi!")
                    dosya = open(str(userid),"w",encoding="utf-8")
                    dosya.write(y.token)
                else:
                    await conv.send_message("Something went wrong. Not sure how though...")
        else:
            await update.reply('Sorry, you are not premium user. If do you want be premium user contact with @' + admin) 


    elif update.message.message == "/start":
            userid = update.message.from_id
            if str(userid) == user_id:
                await update.reply('Nice, You are premium user!') 
            else:
                await update.reply('Sorry, you are not premium user. If do you want be premium user contact with @' + admin) 

    elif update.message.message == "/settings":
       await update.reply('Settings:', buttons=[Button.inline('Delete token', b'token')]) 

try:
    client.start(bot_token=str(bot_token))
    client.add_event_handler(handler)
    print('Successfully started (Press Ctrl+C to stop)')
    client.run_until_disconnected()
finally:
    client.disconnect()
    print('Stopped!')
