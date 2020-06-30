#!/usr/bin/env python3
#coding=utf8
import tushare as ts
from sqlalchemy import create_engine
import pandas
import datetime
import time
import urllib

import databaseConfig
print(databaseConfig.config['connect'])
# import MySQLdb
# 设置数据库参数
engine = create_engine(databaseConfig.config['connect'])
# 表名字
stockBasicInfoTable = 'icb_stock_code'
# 当前日期
currentDate = time.strftime("%Y-%m-%d", time.localtime()) 
# 数据库连接
dbConn = engine.connect()
# 获取当前表中的数据最后的同步日期
sqlSeleteDate = 'SELECT MAX(belong_date) AS belong_date FROM ' + stockBasicInfoTable
oldDate = dbConn.execute(sqlSeleteDate).fetchall()[0][0]
if (oldDate) :
    oldDate = oldDate.strftime("%Y-%m-%d")

# 如果上次的同步日期不是今天， 执行数据同步操作
if (oldDate!= currentDate) :
    try:
        # 获取全部股票列表信息， 保存到数据库
        stockDataFrame = ts.get_stock_basics()
        # 标识本次数据同步日期
        stockDataFrame['belong_date'] = currentDate
        # 插入数据库中
        stockDataFrame.to_sql(stockBasicInfoTable, engine, if_exists='append')
        # 删除旧数据
        sqlDeleteOldData = 'DELETE FROM ' + stockBasicInfoTable + ' WHERE belong_date <=DATE_SUB("' + currentDate + '", INTERVAL 1 YEAR)'
        dbConn.execute(sqlDeleteOldData)
        
    except urllib.error.HTTPError:
        pass
    
exit



