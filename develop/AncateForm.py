#!/usr/bin/env python3
import os,sys,time                   # import modules
import csv

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import ( # 使用するモデル(イベント, メッセージ, アクションなど)を列挙
    MessageEvent, MessageAction,
    TextMessage, TextSendMessage,
    PostbackAction,
    QuickReply, QuickReplyButton,
    URIAction,
    CameraAction,CameraRollAction,
    LocationAction,
    DatetimePickerAction
)



def ReadCSV(csvfile):  
    items = list()
    with open(csvfile) as f: #アンケートファイルを読み込む 
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
                items.append(\
                    {   'Num':row[0],
                        'Quest':row[1],
                        'Choice':row[2:]
                    }
                )
    
    MessageObj = list()
    for quest in items:
        Obj = list()
        for choose in quest['Choice']:
            Obj.append(\
                QuickReplyButton(action=MessageAction(label="{}-{}".format(quest['Num'],choose),
                                text=choose))
            )
        MessageObj.append(TextMessage(text=quest['Quest'], 
                                        quick_reply=QuickReply(items=Obj)))
    return MessageObj
 

