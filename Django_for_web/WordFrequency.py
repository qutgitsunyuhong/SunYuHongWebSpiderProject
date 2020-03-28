# -*- coding: utf-8 -*-

import MySQLdb
import pandas as pd
import jieba
import csv
from collections import Counter

conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='xu332230',db='test2',charset='utf8')
curs = conn.cursor()
sql1 = '''select book_comm1,book_comm2,book_comm3,book_comm4,book_comm5 from  django_web_booklist'''  # sql语句
curs.execute(sql1)
row = curs.fetchall()  # 读取数据表内容，返回元祖类型,元祖的每个元素还是为元祖

data = []
for i in row:
    i = list(i)  # 将元祖的每个元素转换为列表
    new = str(i[0])  # 将列表转换为字符串
    xx = ' '.join(jieba.cut(new))  # 每一段字符串进行分词
    yy = xx.split(' ')
    for j in yy:
        data.append(j)  # 追加写入data列表，得到的数据格式为：a=['我 爱 学习 我 喜欢 北京']

result = dict(Counter(data))
# dict = pd.DataFrame(pd.Series(result), columns=['num'])
# dict = dict.reset_index().rename(columns={'index': 'id'})
# my_result = sorted(result.items(),key=lambda result:result[1],reverse=True)
my_result =dict(sorted(result.items(),key=lambda result:result[1],reverse=True))
# print(my_result)

cnt = 0
truly_result = {}
for key,value in my_result.items():
    cnt=cnt+1
    if cnt <80 :
        pass
    if cnt >=80 and cnt <180:
        truly_result[key] = value
    if cnt>=180:
        break
# print(truly_result)
# with open('out1.csv','w',encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file)
#     for key,value in truly_result.items():
#         writer.writerow([key,value])


# dict.to_csv('out1.csv', encoding='utf-8', header=True)