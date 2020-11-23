from django.shortcuts import render

def sendUse(event):
    try:
        text1 = "Hi"
        message = TextSendMessage(
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='腦子故障中，請稍等 Q_Q'))
