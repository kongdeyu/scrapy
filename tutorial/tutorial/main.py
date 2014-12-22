#!/usr/bin/python
#coding:utf-8

import logging
from scrapy import crawler
from scrapy import log
from scrapy.utils import project
from scrapy import signals
from spiders import youku_spider
from twisted.internet import reactor
from tool import logger


def main():
    # init log
    _ = logger.Logger(30, logging.DEBUG)
    log.start(
        logfile=r'..\log\scrapy.log',
        loglevel=log.INFO,
        logstdout=True)

    # init spider
    spider = youku_spider.YoukuSpider()
    settings = project.get_project_settings()
    crawler = crawler.Crawler(settings)
    crawler.signals.connect(
        reactor.stop,
        signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()


if '__main__' == __name__:
    main()