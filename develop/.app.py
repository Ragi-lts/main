#!/usr/bin/env python3
import os,sys,time,json                   # import modules
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import ( # 使用するモデル(イベント, メッセージ, アクションなど)を列挙
    MessageEvent, MessageAction,
    TextMessage, TextSendMessage, TemplateSendMessage,
    FlexSendMessage, PostbackAction,
    PostbackTemplateAction,
    QuickReply, QuickReplyButton,
    URIAction,
    CameraAction,CameraRollAction,
    LocationAction,
    DatetimePickerAction
)



app = Flask(__name__)

channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)



@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def PostBack(event):
    with open('develop/Ancate_content.json') as f:
        data = json.loads(f.read())
    with open('develop/quickreply.json') as f:
        data2 =f.read()
    
        
    USER = {'Id':event.source.user_id,
            'Name':line_bot_api.get_profile(event.source.user_id).display_name,
            'reply_token':event.reply_token
    }

    messages = TextSendMessage(text='Sample',quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="label", text="text")),
        QuickReplyButton(action=CameraAction(label="Camera")),
        QuickReplyButton(action=LocationAction(label="Location")),
        QuickReplyButton(action=DatetimePickerAction(label="Datetime",mode="time",data="test"))
    ]))
      
    line_bot_api.push_message(USER['Id'], messages=messages)
    return

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
