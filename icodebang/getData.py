#coding=utf8
import tushare as ts
from sqlalchemy import create_engine
import pandas
# import MySQLdb

engine = create_engine('mysql://root:4728999@127.0.0.1/stock?charset=utf8')

code = '002008'
date = '2020-04-10'

# 获取全部股票列表信息， 保存到数据库
# df = ts.get_stock_basics()
# df.to_sql('stock_code', engine, if_exists='append')

# db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='4728999',db="stock",charset="utf8")
# df.to_sql('stock_code',con=db)
# db.close()

# print(df.head(5))

# 获取当日的成交数据
# df = ts.get_today_ticks(code=code)
# print(df.head(5))

# 查询数据库， 获取数据 测试
query = engine.execute('select * from detail_history limit 1')
print(query.fetchall())

sql = 'select * from detail_history limit 2'
# 获取到的数据为 dataframe 格式
data = pandas.read_sql(sql=sql, con=engine)

print(data)

# 获取历史成交明细数据
df = ts.get_tick_data(code=code, date=date, src='nt')
print(df.head(10))
# 添加 股票编码和所属日期
df['code'] = code
df['date'] = date
# 将成交明细存入数据库
# df.to_sql('detail_history',engine,if_exists='append')