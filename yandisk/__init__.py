from telethon import TelegramClient
from yadisk_async import YaDisk
import time
import math
from os import environ
from os.path import exists
from dotenv import load_dotenv

load_dotenv("config.env")

# Telegram
client = TelegramClient("yandisk", environ.get("API_ID"), environ.get("API_HASH"))
admin = environ.get("ADMIN_ID")

# Yandex
yapi_id = environ.get("YANDEX_APP_ID")
yapi_secret = environ.get("YANDEX_APP_SECRET")
token = None

if token is None:
    if exists("token.txt"):
        Yandex = YaDisk(yapi_id, yapi_secret, open("./token.txt", "r").read())
    else:
        Yandex = YaDisk(yapi_id, yapi_secret)
else:
    Yandex = YaDisk(yapi_id, yapi_secret, token)

# Progress 
async def progress(current, total, event, start, type_of_ps):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}]\nPercent: {2}%\n".format(
            ''.join("█" for _ in range(math.floor(percentage / 5))),
            ''.join("░" for _ in range(20 - math.floor(percentage / 5))),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        await event.edit("{}\n {}".format(
            type_of_ps,
            tmp
        ))

def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {
        0: "",
        1: "Ki",
        2: "Mi",
        3: "Gi",
        4: "Ti"
    }
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"
