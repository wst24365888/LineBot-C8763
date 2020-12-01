from urllib import request
import json
from django.conf import settings

def post_data(url, data, headers):
    
    bindata = data if type(data) == bytes else data.encode('utf-8')
    
    req = request.Request(url, bindata, headers=headers)
    resp = request.urlopen(req)
    return resp.read(), resp.getheaders()

def replyGreeting(replyToken):
    greetingMessage = None

    with open("/app/C8763/greeting.json", 'r', encoding='utf8') as f:
        greetingMessage = json.load(f)

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
                                "type": "camera",
                                "label": "開啟相機"
                            }
                        },
                        {
                            "type": "action",
                            # "imageUrl": "https://xxx/image1.png",
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
    print(headers)

    r = post_data("https://api.line.me/v2/bot/message/reply", data, headers)

    print(r)