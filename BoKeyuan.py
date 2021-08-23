# -*- codeing =utf-8 -*-
# @Time :2021/8/23 23:02
# @Author :张玉洁
# @File :BoKeyuan.py
# @Software: PyCharm
import requests
import pymysql
from lxml import etree

conn = pymysql.connect(host='127.0.0.1', user='root', password='zyj191702', port=3306, database='热搜排行榜数据库')
cursor = conn.cursor()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
url = 'https://www.cnblogs.com/'

reponse = requests.get(url, headers=headers)
reponse.encoding = 'utf-8'
html = etree.HTML(reponse.text)

title = html.xpath('//div[@class="post-item-text"]/a/text()')
url1 = html.xpath('//div[@class="post-item-text"]/a/@href')

# sql 中的内容为创建一个名为博客园的表
cursor.execute("drop table if exists 博客园")   # 如果表存在则删除

sql = """create table 博客园(排行 int ,标题 VARCHAR(200),网址 VARCHAR(200))"""    #()中的参数可以自行设置

cursor.execute(sql)    # 创建表


for n in range(len(title)):

    sql = "insert into 博客园(排行,标题,网址) values('%d','%s','%s')"%(n+1,title[n],url1[n])

    cursor.execute(sql)
    conn.commit()

cursor.close()
# 关闭连接
conn.close()
