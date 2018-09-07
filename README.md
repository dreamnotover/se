# seCrawler(Search Engine Crawler)
A scrapy project can crawl search result of Google/Bing/Baidu

## prerequisite
python 2.7， pymysql，sumy and scrapy is needed.
本工程对搜索结果提取摘要，存入mysql数据库中，建表文件在db.sql, query_words关键词抓取后flags置为1.
本爬虫的缺憾是：未能使用代理，抓取一段时间IP会被临时屏蔽。

## commands

run one command to get 50 pages result from search engine with keyword, the result would be kept in the "urls.txt" under the current directory.


####Bing
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=bing -a pages=50```

####Baidu
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=baidu -a pages=50```

####Google
```scrapy crawl keywordSpider -a keyword=Spider-Man -a se=google -a pages=50```

## limitation
The project doesn't provide any workaround to the anti-spider measure like CAPTCHA, IP ban list, etc. 

But to reduce these measures, we recommand to set ```DOWNLOAD_DELAY=10``` in settings.py file to add a temporisation (in second) between the crawl of two pages, see details in [Scrapy Setting](https://doc.scrapy.org/en/1.2/topics/settings.html#std:setting-DOWNLOAD_DELAY).
批量执行  python  batchSpider.py
参考来源 https://github.com/xtt129/seCrawler