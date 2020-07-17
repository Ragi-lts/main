import os
import pandas as pd
from sqlalchemy import create_engine
import random, string



def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def showDB(database,engine):
    return pd.read_sql(sql='SELECT * FROM {};'.format(database), con=engine)

    

# PostgreSQLのサーバー接続エンジンを作成する
engine = create_engine(os.environ['DATABASE_URL'])
code = randomname(10)





col = pd.DataFrame(data = [["YJ",code]],
                   columns=['attendee','authcode']
                   )
col.to_sql('test',con=engine,if_exists='append',index=False)
print(showDB('test',engine))
