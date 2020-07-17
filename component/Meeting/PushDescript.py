import requests
import os
import datetime

def PostDescript(message,typeof='Message'):
    hostid = os.getenv('HOSTTOKEN', None)
    postTo = "https://notify-api.line.me/api/notify"
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    
    header = {
    "Content-Type":'application/x-www-form-urlencoded',
    "Authorization":'Bearer {}'.format(hostid)
    }
    data = {"message":''}
    
    if typeof =='report':
        postdata =[  '\n【不具合報告】',
                    message,
                    '投稿日時:'+now]
    else:
        postdata =[  '\n【意見】',
                    message,
                    '投稿日時:'+now]
    
    data['message'] = '\n'.join(postdata)
    
    r = requests.post(postTo,headers=header,\
                            data=data)
    return r.status_code
    