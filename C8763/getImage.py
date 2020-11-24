import requests

from NCUAI_LineBot import settings

def getImage(messageID):
    print(settings.LINE_CHANNEL_ACCESS_TOKEN)
    print(messageID)
    # 自訂表頭
    my_headers = {'Authorization': "Bearer {}".format(settings.LINE_CHANNEL_ACCESS_TOKEN)}

    # 將自訂表頭加入 GET 請求中
    r = requests.get("https://api.line.me/v2/bot/message/{}/content".format(messageID), headers = my_headers)

    print(r)
    print("aaa")