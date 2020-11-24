import requests

from linebot import LineBotApi

from django.conf import settings

def getImage(messageID):
    r = requests.get(
        'https://api.line.me/v2/bot/message/{messageID}/content', 
        headers = "Authorization: Bearer {}".format(LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN))
    )

    print(r)
    print("aaa")