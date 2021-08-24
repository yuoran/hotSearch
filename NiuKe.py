# -*- codeing =utf-8 -*-
# @Time :2021/8/23 23:04
# @Author :***
# @File :NiuKe.py
# @Software: PyCharm
import time
import requests
import pymysql
from lxml import etree
while True:
    time_now = time.strftime("%M:%S",time.localtime())
    if time_now == "30:10":
        conn = pymysql.connect(host='127.0.0.1', user='root', password='*****', port=3306, database='热搜排行榜数据库')
        cursor = conn.cursor()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"
        }
        url = 'https://www.nowcoder.com/discuss?order=1&type=0&expTag=0'

        reponse = requests.get(url, headers=headers)   # reponse
        html = etree.HTML(reponse.text)

        url1 = html.xpath('//div[@class="discuss-main clearfix"]/a[@rel="prefetch"]/@href')
        title = html.xpath('//div[@class="discuss-main clearfix"]/a[@rel="prefetch"]/text()')

        for i in range(title.count('\n')):
            title.remove('\n')

        # sql 中的内容为创建一个名为牛客的表
        cursor.execute("drop table if exists 牛客")   # 如果表存在则删除

        sql = """create table 牛客(排行 int ,标题 VARCHAR(200),网址 VARCHAR(200))"""   #()中的参数可以自行设置

        cursor.execute(sql)    # 创建表


        for n in range(len(url1)):

            url2 = 'https://www.nowcoder.com/'+url1[n]
            sql = "insert into 牛客(排行,标题,网址) values('%d','%s','%s')"%(n+1,title[n],url2)
            cursor.execute(sql)
            conn.commit()

        cursor.close()
        # 关闭连接
        conn.close()
        time.sleep(2)
