# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import  Selector
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import pymysql
import MySQLdb
from goose import Goose
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com','google.com','baidu.com']
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None
    g = Goose()

    def __init__(self, keyword, se = 'bing', pages = 2,  *args, **kwargs):
        super(keywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]        
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)
            

    def parse(self, response):
        connection = pymysql.connect(
        host='192.168.101.186',  # 连接的是本地数据库
        user='root',        # 自己的mysql用户名
        passwd='123456',  # 自己的密码
        db='adskeywordtextdb',      # 数据库的名字
        charset='utf8',     # 默认的编码方式：
        cursorclass=pymysql.cursors.DictCursor)        
        try:
            with connection.cursor() as cursor:
                for url in Selector(response).xpath(self.selector).extract():
                    yield {'url':url}
                    
                    # 数据库表的sql
                    article=self.g.extract(url=url) 
                    #print article.title[0:100],article.cleaned_text[:150]                    
                    content=''.join(article.cleaned_text)
                    title=article.title
                    fulltext = MySQLdb.escape_string(content);
                    if  len(content)<100  or  len(url) >254 or  len(fulltext)> 16777215 :
                       continue
                    summary_abstract=  MySQLdb.escape_string( self.get_summary(content))
                    sql = 'Insert into keywordtexts(url,keyword,title,article,summary) values (\'%s\' ,\'%s\' ,\'%s\' ,\'%s\',\'%s\')' % ( url, self.keyword,MySQLdb.escape_string(title),fulltext,summary_abstract)

                    tail='ON DUPLICATE KEY UPDATE  article=values(article),summary=values(summary),title=values(title)'
                    sql = sql+tail
                    print( sql)
                    cursor.execute(sql)
            
                    # 提交本次插入的记录
                    connection.commit()
                pass 
        except Exception as err:  
            print(err)            
            
                
        finally:
                # 关闭连接
                connection.close()
                
    
    def get_summary(self, docment_text):
        LANGUAGE = "english"
        SENTENCES_COUNT = 20
        summary_sent=[]
        parser = PlaintextParser.from_string(docment_text, Tokenizer(LANGUAGE))  
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary_sent.append(str(sentence))
        output= ''.join(summary_sent)
        return output
                
