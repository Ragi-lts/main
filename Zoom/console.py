from . import PostServer as MeetingSet
import datetime
from pprint import pprint
import json,re
import sys



data = {
    "topic": str(),             # 題名 (必須)
    "type": int(),              # 1:即時、2:スケジュール (必須)
    "start_time": str(),        # 開始時間"yy-mm-ddTHH:mm:ssZ"
    "duration": str(),          # type:2 only ) [minutes] 
    "password": str(),          # パスワードを設定する場合指定
    "agenda": str(),            # 趣旨(任意)
    "timezone": "Asia/Tokyo"
}

setting = {
    "host_video": "true",        # 開始時に主催者のビデオをオンにするか
    "participant_video": "true", # 開始時に参加者のビデオもオンにするか
    "join_before_host": "true",  #主催者が参加する前に参加できるか(type:2) 
    "auto_recording": "none",      # 録画するかどうか[local,cloud,none]
    "enforce_login": "false"     # サインインした人のみ会議に参加するか
}


def setMeeting():
    # print("ミーティングリストを取得しています...")
    # print("*"*50)
    # res = MeetingSet.getList()
    # pprint(res)
    # print("*"*50)
    
    
    temp = data
    temp_s = setting
    try:
        ask(temp,temp_s)
        while(not confirm(temp,temp_s)):
            temp = data
            temp_s = setting
            ask(temp,temp_s)
            
        print('''
        以上で設定完了です。
        ''')
        
        temp['settings']=temp_s
        pprint(temp)
    
        res = MeetingSet.Create(temp)
        print("*"*50)
        pprint(res)
        # print("ミーティングリストを取得しています...")
        # detail = MeetingSet.getList()
        # pprint(detail)
     

        
        
          
            
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        sys.exit()

    return res

def error():
    return print('データが間違っているか、質問に答えていません。')

def true_yes(value):
    if value == 'true': return 'Yes'
    else : return 'No'
    
def date_check(value):
    try:
        now  = datetime.datetime.now()
        dateat = datetime.datetime.strptime(value,'%Y/%m/%d %H:%M:%S')
        sub = int((dateat - now).total_seconds())
        if sub > 0:
            return dateat.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            print('正常な日時ではありません。')
            return False
        
    except ValueError:
            error()
            return False
        
def choice(key,data):
    try:
        if key in range(len(data)):
            value = key
            key = data[value]
    except :
        return None

           
    
def ask(data,setting):
    
    print(' Zoomの会議を設定します。')
    print("-"*50)


    while(len(data['topic']) == 0):
        data['topic'] = input("会議名を入力 \t>>")
      
    while(data['type'] not in ['1','2']):
        data['type'] = input("""会議の開始形式を選択してください。
        即時開催:1\t    時間指定:2 \t>> """)
        if data['type']  not in ['1','2'] : error()
        
    if data['type'] == '2':
        while(1):
            now = datetime.datetime.now()
            data['start_time'] = input("""
            開始時間を入力してください。
            (入力方式)\t yyyy/mm/dd HH:MM:SS
            （入力例）\t {}
            \t\t>>""".format(now.strftime('%Y/%m/%d %H:%M:%S')))
            data['start_time'] = date_check(data['start_time'])
            if  data['start_time']!= False: break
                
            
        data['duration'] = input("""
        開催時間の長さを入力してください。[Minutes]
        必要がなければEnterを押してください。\t>>""")
        
        data['password'] = input("""
        設定するパスワードを入力してください。
        必要がなければEnterを押してください。\t>>""")
        
    difficulty =input("""
    会議の詳細設定を行いますか?(y/N)
    必要がなければEnterを押してください。\t>>""")

    if difficulty == 'y':
        setting['auto_recording'] = input("""
        この会議を録画しますか?
        1:クラウド上\t 2:自分のコンピュータ
        必要がなければEnterを押してください。\t>>""")
        choice(setting['auto_recording'],
               ['','cloud','local'])
      
        setting['enforce_login'] = input("""
        この会議はサインインした人のみが入れるようにしますか? (y/N)
        必要がなければEnterを押してください。\t>>""")
        if ( setting['enforce_login'] == 'y'): log = 'true'
      
        setting['join_before_host'] = input("""
        会議開始前に参加者が会議に参加できるようにしますか? (y/N)
        必要がなければEnterを押してください。\t>>""")
        if setting['join_before_host'] == 'y': setting['join_before_host'] = 'true'
     

        
        setting['host_video'] = input("""
        会議開始時に主催者がビデオをオンにした状態で参加しますか? (y/N)
        必要がなければEnterを押してください。\t>>""")
        if setting['host_video'] == 'y': setting['host_video'] = 'true'
      
         
        setting['participant_video'] = input("""
        会議開始時に参加者がビデオをオンにした状態で参加しますか? (y/N)
        必要がなければEnterを押してください。\t>>""")
        if setting['participant_video'] == 'y':  setting['participant_video'] = 'true'

    return 
    # return  json.dumps(data)

def confirm(data,setting):
    meetingtype = str()
    inmeet = str()
    rec = str()
    
    if data['type'] == '1':
        meetingtype = '即時開催'
    elif data['type'] == '2':
        meetingtype = '時間指定\t({}開始)'.format(re.sub('[T|Z]',' ',data['start_time']))
        
    if setting['enforce_login'] in ['false','']:
        inmeet = '全体公開'
    elif  setting['enforce_login'] == 'true':
        inmeet = 'アカウント保持者のみ'
        
    if setting['auto_recording'] in ['none','']:
        rec = 'なし'
    elif setting['auto_recording'] == 'cloud':
        rec = 'Cloudに保存'
    elif setting['auto_recording'] == 'local':
        rec = '本体に保存'
   
   

        
    
    print("-"*50)

    print("""
    会議名:\t\t{}
    """.format(data['topic']))

    print("""
    開催方式:\t\t{}
    """.format(meetingtype))

    if data['type'] == 2:
        print("""
        開催時間(予定):\t\t{}分
        """.format(data['duration']))
        
    print("""
    設定したパスワード:\t\t{}
    """.format(data['password']))
    print("-"*50)
    
    print("""
    録画設定:\t\t{}
    """.format(rec))

    print("""
    公開範囲:\t\t{}
    """.format(inmeet))
    print("-"*50)    

    print("""
    開始時に主催者のビデオをオン:\t{}
    """.format(true_yes(setting['host_video']) ))
   
    print("""
    開始時に参加者のビデオをオン:\t{}
    """.format(true_yes(setting['participant_video']) ))
   
    print("-"*50)
 
    isok = input('これで間違いないですか? (y/N) \t>>')
    if isok.lower() in ['y','']:
        return True
     
    
if __name__ == '__main__':
    setMeeting()


