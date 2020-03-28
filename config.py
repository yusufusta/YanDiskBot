import os

BOTTOKEN = os.environ.get("BOTTOKEN", "")
APIID = int(os.environ.get("APIID", 6))
APIHASH = os.environ.get("APIHASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
ADMINID = os.environ.get("ADMINID", "452321614")
ADMINUSERNAME = os.environ.get("ADMINUSERNAME", "quiec")

YANDEXAPPID = os.environ.get("YANDEXAPPID", "")
YANDEXAPPSECRET = os.environ.get("YANDEXAPPSECRET", "")

"""
If you using VPS, edit like this:
BOTTOKEN = "123456:xxxx"
APIID = 6
APIHASH = eb06d4abfb49dc3eeb1aeb98ae0f581e
"""
