#!/usr/bin/env python3
import os,sys,time                   # import modules
import requests,json


BASEURL = 'https://api.zoom.us/v2/users/'
HOSTID = os.getenv('Zoom_HOSTID', None)
API_Key = os.getenv('Zoom_API_Key', None)
API_Secret = os.getenv('Zoom_API_Secret', None)

MEETING_URL = BASEURL + HOSTID +'/meetings'

def generate_JWT():             # JWTトークンの生成
    import http.client
    import base64
    import time
    import hmac
    import hashlib
    
    expiration = int(time.time()) + 5 # 有効期間5秒
    
    header    = base64.urlsafe_b64encode('{"alg":"HS256","typ":"JWT"}'.encode()).replace(b'=', b'') # ヘッダー
    payload   = base64.urlsafe_b64encode(('{"iss":"'+API_Key+'","exp":"'+str(expiration)+'"}').encode()).replace(b'=', b'') # APIキーと>有効期限
    
    hashdata  = hmac.new(API_Secret.encode(), header+".".encode()+payload, hashlib.sha256) # HMACSHA256でハッシュを作成
    signature = base64.urlsafe_b64encode(hashdata.digest()).replace(b'=', b'') # ハッシュをURL-Save Base64でエンコード
    token = (header+".".encode()+payload+".".encode()+signature).decode()  # トークンをstrで生成
    return token

def getList():
    Meeting_Data = list()       # 会議の予定データ
    JWT_TOKEN = generate_JWT()  # JWT Token
    
    headers = {'Authorization':'Bearer' + JWT_TOKEN}
    r =  requests.get(MEETING_URL,headers=headers)
    r = json.loads(r.text)      # Response
    
    for i in r['meetings']:
        Meeting_Data +=[{'Topic':i['topic'],
                         'URL':i['join_url'],
                         'RoomID':i['id'],
        }]
            
    return Meeting_Data


def Create(data=None):
        if data == None : return sys.exit(1)
        else:
            JWT_TOKEN = generate_JWT()            
            headers = {
                'Content-Type':'application/json',
                'Authorization':'Bearer' + JWT_TOKEN
            }
            
            data = json.dumps(data).encode('utf-8')
            
            r =  requests.post(MEETING_URL,data=data,headers=headers)
            r = json.loads(r.text)
          
            Meeting_Data = {'Topic':r['topic'],
                            'URL':r['join_url'],
                            'RoomID':r['id'],
                            'Password':r['password'],
                            'StartTime':r['start_time'],
                            'Duration':r['duration']
            }
            # print(Meeting_Data)
            
            return Meeting_Data
