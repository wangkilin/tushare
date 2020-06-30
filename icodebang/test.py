#!/usr/bin/python3
str = 'iCodebang'
print (str)             # 输出字符串
print (str[0:-1])       # 输出第一个到倒数第二个的所有字符
print (str[0])          # 输出字符串第一个字符
print (str[2:5])        # 输出从第三个开始到第五个的字符
print (str[2:])         # 输出从第三个开始的后的所有字符
print (str * 2)         # 输出字符串两次，也可以写成 print (2 * str) 
print (str + "TEST")    # 连接字符串

dict = {'Name': 'iCodebang', 'Age': 7}
for key in dict:
    print(key)
list = ['a', 1, 'c']
for value in list:
    print(value)

dictList = [{'name':'name1'}, {'name':'name2'}]
print("dictList length is:",len(dictList))
dictListLength = len(dictList)
for index in range(dictListLength):
    dictList[index]['age'] = index
#dictList['age'] = 20
print(dictList)