#!/usr/bin/python
#coding:utf-8

import logging
from twisted.internet import reactor
from scrapy import log
from scrapy import signals
from scrapy import crawler
from scrapy.utils import project
from spiders import youku_spider
from tool import logger

if '__main__' == __name__:
    # init log
    _ = logger.Logger(30, logging.DEBUG)
    log.start(logfile = r'..\log\scrapy.log',
              loglevel = log.INFO,
              logstdout = True)
    # init spider
    spider = youku_spider.YoukuSpider()
    settings = project.get_project_settings()
    crawler = crawler.Crawler(settings)
    crawler.signals.connect(reactor.stop,
                            signal = signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()