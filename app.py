import urllib.request
import os
import sys,time
import json
from argparse import ArgumentParser
from component.Meeting import ScheduleNortify

from cryptography.fernet import Fernet

from flask import Flask, request, abort
from flask_bootstrap import Bootstrap
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import ( # 使用するモデル(イベント, メッセージ, アクションなど)を列挙
    MessageEvent, MessageAction,
    TextMessage, TextSendMessage, TemplateSendMessage,
    FlexSendMessage, 
    ConfirmTemplate,
    PostbackEvent, PostbackAction,
    PostbackTemplateAction,
    QuickReply, QuickReplyButton,
    URIAction,
    CameraAction,CameraRollAction,
    LocationAction,
    DatetimePickerAction,
    URITemplateAction,
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds
)


app = Flask(__name__)
bootstrap = Bootstrap(app)


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


def NonStopObj(file):
    rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=800, height=270),
    selected=True,
    name="Sample RichMenu",
    chat_bar_text="不具合などがある場合",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=800, height=270),
        action= PostbackAction(
                label='不具合の報告・意見',
                display_text='不具合の報告・意見があります',
                data="action=report"
            )
        )]
        )

    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(rich_menu_id)
    with open (file, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id,'image/png',f)
        line_bot_api.set_default_rich_menu(rich_menu_id)
    return 


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
        
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(PostbackEvent)
def PostBack(event):
    import re
    USER = {'Id':event.source.user_id,
            'Name':line_bot_api.get_profile(event.source.user_id).display_name,
            'reply_token':event.reply_token
    }      
    report = re.match('action=report*',event.postback.data)    
    
    if event.postback.data == "attend":
        send_DetailMeeting(USER)
    elif report:
        Report_Trouble(event,USER)
    return 
    
def send_DetailMeeting(USER):
    with open("data/reserve","rb") as f,\
        open("data/.key","rb") as k:
        data = f.read()
        key_dec = k.read()
        dec_obj = Fernet(key_dec)
        
        meeting = json.loads(dec_obj.decrypt(data))
        
        data = ScheduleNortify.NortifyRoomId(USER['Name'],
                                            meeting['RoomID'],
                                            meeting['Password'],
                                            meeting['URL'])
        payload = FlexSendMessage(
            alt_text='参加登録ありがとうございます。',
            contents=data
        )
        line_bot_api.push_message(USER['Id'],
                                payload)
        return

def Report_Trouble(event,USER):
    attention = "下の項目から、不具合の報告・その他のどちらかを選んでください。"
    
    if event.postback.data == "action=report":
        line_bot_api.push_message(USER['Id'],
                                    TextSendMessage(text=attention,
                                                    quick_reply=\
                                    QuickReply(items=[\
                                    QuickReplyButton(action= PostbackAction(
                                                            label='不具合の報告',
                                                            display_text='不具合の報告',
                                                            data='action=report&bug'
                                                        )),
                                                        
                                    QuickReplyButton(action= PostbackAction(
                                                            label='その他',
                                                            display_text='その他',
                                                            data='action=report&any'
                                                        ))
                                        ])
                                    )
                                )
        return
    elif event.postback.data == "action=report&bug" or event.postback.data == "action=report&any":
        if event.postback.data == "action=report&bug":
            line_bot_api.reply_message(USER['reply_token'],
                                    TextSendMessage(text="不具合の報告ですね。"))
        elif event.postback.data == "action=report&any":
            line_bot_api.reply_message(USER['reply_token'],
                                    TextSendMessage(text="おっ、ありがとうございます〜"))
        confirm_message = TemplateSendMessage(
                                                        alt_text='OpenWebPage?',
                                                        template=ConfirmTemplate(
                                                        text='入力用のWebページを起動しますか？（誤っていいえを選択した場合でも、はいを押すことで起動できます）',
                                                        actions=[
                                                            URIAction(label='はい',
                                                                    uri='https://liff.line.me/1654337169-rzoplDmp'),
                                                            PostbackAction(
                                                            label='いいえ',
                                                            display_text='いいえ',
                                                            data='action=report&cancel')
                                                        ]
                                                    )
                                                ) 
        line_bot_api.push_message(USER['Id'],confirm_message)
    elif event.postback.data == "action=report&cancel":
        line_bot_api.push_message(USER['Id'],
                                    TextSendMessage(text="取り消しました。"))  
    return 



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    USER = {'Id':event.source.user_id,
            'Name':line_bot_api.get_profile(event.source.user_id).display_name,
            'reply_token':event.reply_token
    }
    message = event.message.text
    return 



if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
#    NonStopObj("component/Images/richMenu_Trouble.png")
    app.debug=True
    app.run(host="0.0.0.0", port=port)
