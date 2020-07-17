import json
from datetime import datetime

def NortifyMeeting(topic,date,endfor): # date is type of datetime
    if topic == None or date == None: return

    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    endhour = endfor.hour
    endminute = endfor.minute
    
    data =\
        {
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "お知らせです",
                        "weight": "bold",
                        "size": "lg",
                        "align": "center",
                        "contents": []
                    },
                    {
                        "type": "separator",
                        "margin": "none"
                    },
                    {
                        "type": "text",
                        "margin": "sm",
                        "text": "以下の日時で{}を開催します。".format(topic),
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "参加したい方は以下の\"参加する\"のボタンをタップしてください。",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "開始時間に開催できるようにしておりますが、諸事情により開催時間が遅れる場合があります。",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "spacer",
                                "size": "lg"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "開催日",
                                        "color": "#aaaaaa",
                                        "size": "md",
                                        "flex": 2,
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "{:04}/{:02}/{:02}".format(year,
                                                                           month,
                                                                           day),
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "md",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "開始時間",
                                        "color": "#aaaaaa",
                                        "size": "md",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": "{:02}:{:02}".format(hour,
                                                                     minute),
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "md",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "終了時間",
                                        "color": "#aaaaaa",
                                        "size": "md",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": "{:02}:{:02}".format(endhour,
                                                                     endminute),
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "md",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "spacer",
                                "size": "lg"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "spacer",
                                "size": "xl"
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "action": {
                                    "type": "postback",
                                    "label": "参加する",
                                    "data": "attend",
                                    "displayText": "参加します"
                                }
                            },
                            {
                                "type": "spacer",
                                "size": "xl"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "無効なIDと表示された場合、会議は終了しています。",
                        "wrap": True,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "個別質問対応に対する機能は開発中です。",
                        "wrap": True,
                        "align": "center"
                    }
                ]
            }
        }
    return data


def NortifyRoomId(name,roomid,password,url):
    data =  \
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "参加ありがとうございます。",
                        "weight": "bold",
                        "size": "lg",
                        "align": "center",
                        "wrap": True,
                        "contents": []
                    },
                    {
                        "type": "separator",
                        "margin": "none"
                    },
                    {
                        "type": "text",
                        "text": "{}さん".format(name),
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "margin": "lg",
                        "text": "会議の詳細情報を送りますので、取扱いにはご注意ください。よろしくお願いします。",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "margin": "lg",
                        "text": "開始時間になっても入室できない場合は、ご連絡ください。",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "spacer"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "ルームID",
                                        "color": "#aaaaaa",
                                        "size": "xs",
                                        "flex": 2,
                                        "wrap": True,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "{}".format(roomid),
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "パスワード",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "{}".format(password),
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "separator"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "none",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "URL",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "{}".format(url),
                                        "wrap": True,
                                        "color": "#6495ED",
                                        "size": "sm",
                                        "flex": 5,
                                        "decoration": "underline",
                                        "action": {
                                            "type": "uri",
                                            "label": "action",
                                            "uri": "{}".format(url)
                                        }
                                    }
                                ],
                                "margin": "xxl"
                            }
                        ],
                        "margin": "lg"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "spacer",
                        "size": "sm"
                    }
                ],
                "flex": 0
            }
        }
    return data




    

