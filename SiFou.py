# -*- codeing =utf-8 -*-
# @Time :2021/8/23 23:00
# @Author :****
# @File :SiFou.py
# @Software: PyCharm
import requests
import pymysql
from lxml import etree

conn = pymysql.connect(host='127.0.0.1', user='root', password='******', port=3306, database='热搜排行榜数据库')

cursor = conn.cursor() #获取对应的操作游标


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
url = 'https://segmentfault.com/blogs'

reponse = requests.get(url, headers=headers)   # reponse
reponse.encoding = 'utf-8'
html = etree.HTML(reponse.text)

title = html.xpath('//div[@class="content"]/h5/a/text()')
url1 =html.xpath('//div[@class="content"]/h5/a/@href')

# sql 中的内容为创建一个名为思否的表
cursor.execute("drop table if exists 思否") # 如果表存在则删除

sql = """create table 思否(排行 int ,标题 VARCHAR(200),网址 VARCHAR(200))""" #()中的参数可以自行设置

cursor.execute(sql)  # 创建表

for n in range(len(title)):
    url2='https://segmentfault.com/blogs'+url1[n]
    #print(url2)
    sql = "insert into 思否(排行,标题,网址) values('%d','%s','%s')"%(n+1,title[n],url2)
    cursor.execute(sql)
    conn.commit()

cursor.close()
# 关闭连接
conn.close()
