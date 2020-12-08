import json
import random

from urllib import request
from django.conf import settings

def post_data(url, data, headers):
    
    bindata = data if type(data) == bytes else data.encode('utf-8')
    
    req = request.Request(url, bindata, headers=headers)
    resp = request.urlopen(req)
    return resp.read(), resp.getheaders()

def replyGreeting(replyToken, usageCounter):
    greetingMessage = None

    with open("/app/C8763/greeting.json", 'r', encoding='utf8') as f:
        greetingMessage = json.load(f)
        f.close()

    # gifs = ["https://imgur.com/U8nbxfa.gif", "https://imgur.com/uGGaVZP.gif", "https://imgur.com/wGz2pqK.gif"]
    pics = ["https://i.ytimg.com/vi/paIuEIufGyw/maxresdefault.jpg", "https://i.ytimg.com/vi/B_AABV9KUQY/maxresdefault.jpg", "https://imgur.com/LpNni5L.jpg", "https://imgur.com/LpNni5L.png", "https://imgur.com/LpNni5L"]

    greetingMessage["hero"]["url"] = pics[random.randint(0,4)]
    greetingMessage["footer"]["contents"][1]["contents"][0]["text"] = str(usageCounter)
    greetingMessage["footer"]["contents"][2]["contents"][0]["text"] = "({}%)".format(int(usageCounter*100/48763))
    greetingMessage["footer"]["contents"][2]["contents"][1]["contents"][0]["width"] = "{}%".format(int(usageCounter*100/48763))

    data = json.dumps({
        "replyToken": replyToken,
        "messages": [
            {
                "type": "flex",
                "altText": "您有星爆訊息",
                "contents": greetingMessage,
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            # "imageUrl": "https://xxx/image1.png",
                            "action": {
                                "type": "message",
                                "label": "使用說明",
                                "text": "使用說明"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "camera",
                                "label": "開啟相機"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "cameraRoll",
                                "label": "開啟相簿"
                            }
                        },
                    ]
                }
            }
        ],
    })

    headers = {
        'Content-Type':'application/json', 
        "Authorization": "Bearer {}".format(settings.LINE_CHANNEL_ACCESS_TOKEN)
    }

    print(data)
    # print(headers)

    r = post_data("https://api.line.me/v2/bot/message/reply", data, headers)

    print(r)