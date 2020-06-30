前段时间玩Python时无意看到了获取股票交易数据的tushare模块，由于自己对股票交易挺有兴趣，加上现在又在做数据挖掘工作，故想先将股票数据下载到数据库中，以便日后分析：

# 导入需要用到的模块
from queue import Queue
import threading
import os
import datetime

import tushare as ts
from sqlalchemy import create_engine
from sqlalchemy import types
# 创建myql数据库引擎，便于后期链接数据库
mysql_info = {'host':'localhost','port':3306,'user':'******','passwd':'******','db':'stock','charset':'utf8'}
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' %(mysql_info['user'],mysql_info['passwd'],
                                                             mysql_info['host'],mysql_info['port'],
                                                             mysql_info['db'],mysql_info['charset']),
                       echo=False)
# 获取所有股票数据，利用股票代码获取复权数据
stock_basics = ts.get_stock_basics()
stock_basics.columns
# 获取数据库现有数据的时间日期
def get_old_date():
    con = engine.connect()
    sql1 = 'show tables;'
    tables = con.execute(sql1)
    if ('fq_day',) not in tables:
        date_old = datetime.date(2001,1,1)
        return date_old
    sql2 = 'select max(date) from fq_day;'
    date_old = con.execute(sql2).fetchall()[0][0].date()
    if date_old < datetime.date.today() - datetime.timedelta(1):
        return date_old
    else:
        con.close()
        print('今天已经获取过数据，不需重新获取')
        os._exit(1)
# 声明队列，用于存取股票以代码数据，以便获取复权明细
stock_code_queue = Queue()
for code in stock_basics.index:
    stock_code_queue.put(code)

type_fq_day = {'code':types.CHAR(6),'open':types.FLOAT,'hige':types.FLOAT,'close':types.FLOAT,'low':types.FLOAT,
              'amount':types.FLOAT,'factor':types.FLOAT}
# 获取复权数据
def process_data(old_date,task_qeue):
    #queueLock.acquire()
    while not task_qeue.empty():
        data = task_qeue.get()
        print("正在获取%s;数据还有%s条:" %(data,task_qeue.qsize()))
        #queueLock.release()
        date_begin = old_date + datetime.timedelta(1)
        date_end = datetime.date.today()
        try:
            qfq_day = ts.get_h_data(data,start = str(date_begin),end=str(date_end),autype='qfq',drop_factor=False)
            qfq_day['code'] = data
            qfq_day.to_sql('fq_day',engine,if_exists='append',dtype=type_fq_day)
        except:
            task_qeue.put(data)  # 如果数据获取失败，将该数据重新存入到队列，便于后期继续执行
    #else:
        #queueLock.release()
昨天试了下单线程下载股票数据，但由于获取数据量较大，所需时间特别长，这次用多线程实试试

# 重写线程类，用户获取数据
class get_qfq(threading.Thread):
    
    def __init__(self,name,queue,date_begin):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.begin = date_begin
    def run(self):
        process_data(self.begin,self.queue)
        print("Exiting " + self.name)
        
# 声明线程锁
#queueLock = threading.Lock()
old_date = get_old_date()
# 生成10个线程
threads = []
for i in range(7):
    thread = get_qfq('thread'+ str(i), stock_code_queue,old_date)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
正在获取300239;数据还有718条:
[Getting data:]##正在获取002042;数据还有717条:
[Getting data:]正在获取600999;数据还有716条:
[Getting data:]正在获取300453;数据还有715条:
[Getting data:]#正在获取600538;数据还有714条:
[Getting data:]###正在获取002253;数据还有713条:
[Getting data:]正在获取600188;数据还有712条:
[Getting data:]正在获取000948;数据还有711条:
[Getting data:]###正在获取002586;数据还有710条:
[Getting data:]正在获取002651;数据还有709条:
[Getting data:]正在获取600705;数据还有708条:
[Getting data:]##正在获取300135;数据还有707条:
[Getting data:]##正在获取600755;数据还有706条:
[Getting data:]正在获取601890;数据还有705条:
[Getting data:]正在获取300341;数据还有704条:
[Getting data:]#正在获取000897;数据还有703条:
[Getting data:]###正在获取600886;数据还有702条:
[Getting data:]#正在获取002015;数据还有701条:
[Getting data:]正在获取600662;数据还有700条:
[Getting data:]#正在获取000408;数据还有699条:
[Getting data:]#正在获取000524;数据还有698条:
[Getting data:]#正在获取300309;数据还有697条:
[Getting data:]#正在获取600333;数据还有696条:
[Getting data:]##正在获取002178;数据还有695条:
本次采用了10个线程，下载速度快了许多，查看了下流量，基本可以达到3M/S，是单线程的6倍左右。