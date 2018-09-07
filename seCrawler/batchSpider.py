# -*- coding: utf-8 -*-

 
import pymysql
import MySQLdb
 
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
 
connection = pymysql.connect(
host='192.168.101.186',  # 连接的是本地数据库
user='root',        # 自己的mysql用户名
passwd='123456',  # 自己的密码
db='adskeywordtextdb',      # 数据库的名字
charset='utf8',     # 默认的编码方式：
cursorclass=pymysql.cursors.DictCursor)  
cursor = connection.cursor()
cursor.execute('select id,keyword from query_words where flags=0')

for data in cursor.fetchall():

    cmd="scrapy crawl  keywordSpider -a keyword='%s' -a se=bing -a pages=10  -s LOG_FILE=scrapy.log  " %data['keyword']
    print(  cmd)     
    os.system(cmd)
    cursor.execute("update  query_words set flags=1 where id=%s" %data['id'])

cursor.close()  
connection.close() 
exit()   
