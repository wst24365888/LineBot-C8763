import requests

from linebot import LineBotApi

from django.conf import settings

def getImage(messageID):
    # 自訂表頭
    my_headers = {'Authorization': "Bearer {}".format(LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN))}

    # 將自訂表頭加入 GET 請求中
    r = requests.get('https://api.line.me/v2/bot/message/{messageID}/content', headers = my_headers)

    print(r)
    print("aaa")