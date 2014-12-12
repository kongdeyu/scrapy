# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging
import scrapy
import items
from tool import redis_manager

log = logging.getLogger()

class YoukuSpider(scrapy.Spider):
    name = "youku"
    allowed_domains = ["youku.com"]
    start_urls = [
        "http://www.youku.com/",
    ]
    
    def __init__(self):
        try:
            self.redis = redis_manager.RedisManager(rhost = '10.81.14.171',
                                            rport = 8888)
        except redis_manager.Error as e:
            log.critical('e:%s, connect to redis fail' %(e))
            exit()

    def parse(self, response):
        for sel in response.xpath(
            '//div[@class="v v-large focusVideo ishover"]'
            '| //div[@class="v ishover"]'):
            log.debug('sel:%s' %(sel))
            item = items.YoukuItem()
            # get title, filter invalid item
            item['title'] = sel.xpath('div[@class="v-link"]'
                                      '/a'
                                      '/@title[1]').extract()
            if not item['title']:
                log.warning('sel:%s, no title' %(sel))
                continue

            # get href, filter invalid item
            item['href'] = sel.xpath('div[@class="v-link"]'
                                     '/a'
                                     '/@href[1]').extract()
            if not item['href']:
                log.warning('sel:%s, no href' %(sel))
                continue

            # get image_urls, filter invalid item
            item['image_urls'] = sel.xpath('div[@class="v-thumb"]'
                                           '/img'
                                           '/@_src[1]').extract()
            # no _src, then get src
            if not item['image_urls']:
                item['image_urls'] = sel.xpath('div[@class="v-thumb"]'
                                               '/img'
                                               '/@src[1]').extract()
            if not item['image_urls']:
                log.warning('sel:%s, no image_urls' %(sel))
                continue

            # filter repeated item
            if self.redis.hexists('hrefs', item['href'][0]):
                log.info('href:%s, repeated item' %(item['href'][0]))
            else:
                self.redis.hset('hrefs', item['href'][0], 1)
                log.info('title:%s, href:%s, image_urls:%s'\
                         %(item['title'], item['href'], item['image_urls']))
                yield item