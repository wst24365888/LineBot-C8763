from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from . import getImage
from . import imgurUpload
from C8763_Overlay import C8763 as filter_C8763
from PIL import Image

import os

imgur_client = imgurUpload.setauthorize()
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def saveImg(messageId, img_rgb):
    img = Image.fromarray(img_rgb, 'RGBA')
    img.save("{}.png".format(messageId))

def uploadImage(filename, path):
    config = {
        'name': filename,
        'title': filename,
        'description': 'C8763'
    }

    imageInfo = imgurUpload.upload(imgur_client, path, config)
    print(imageInfo['link'])
    
    try:
        os.remove(path)

    return imageInfo['link']

@csrf_exempt
def callback(request): 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            print(event)
            img_rgb = getImage.getImageFromID(event.message.id)
            # saveImg(event.message.id, img_rgb)
            saveImg(event.message.id, filter_C8763.getC8763Overlay(img_rgb))
            link = uploadImage(event.message.id, "/app/{}.png".format(event.message.id))
            
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=link)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()