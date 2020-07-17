#!/usr/bin/env python3
import os,sys,time                   # import modules

import os,sys
import subprocess
from component.Meeting import ScheduleNortify
from datetime import datetime,timedelta
from Zoom import console

from cryptography.fernet import Fernet


#####################################################################
meeting_data = console.setMeeting()

topic = meeting_data['Topic']
end_at = meeting_data['StartTime']
#Ex)2020/05/31 10:00

######################################################################
start = datetime.strptime(meeting_data['StartTime'], '%Y-%m-%dT%H:%M:%SZ')\
    +timedelta(hours=9)
end = start + timedelta(minutes=int(meeting_data['Duration']))
    # 開始、終了時間

if start > end :
    print("エラーがあります")
    sys.exit(1)
    
define = ScheduleNortify.NortifyMeeting(\
                                        topic, # 主題
                                        start,
                                        end
)

import urllib.request

import json
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,
    MessageAction,
    FlexSendMessage, BubbleContainer, CarouselContainer, TextSendMessage
)


channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
    if channel_access_token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')

def main():
    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)
    
        
   
    flex_message = FlexSendMessage(
        alt_text='会議開催のお知らせです。',
        contents=define
    )   
    
    if line_bot_api.broadcast(flex_message) :
        print("Send Success!")


def Encrypt_METJSON():
    key = Fernet.generate_key()
    enc_obj = Fernet(key)

    data = enc_obj.encrypt(json.dumps(meeting_data).encode('utf-8'))
    with open("data/reserve","wb") as f,\
         open("data/.key","wb") as k:
        f.write(data)
        k.write(key)
    return 
        

if __name__ == '__main__':
    if input("送信OK? [Enter / else] >>\t")  in  ['y','']:
        Encrypt_METJSON()
        shell = 'update.sh'
        subprocess.call( ['sh',shell], cwd=os.getcwd())
        main()

    
