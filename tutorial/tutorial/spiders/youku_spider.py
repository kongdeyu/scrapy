# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging
import scrapy
import items


add = lambda x : x + 1


log = logging.getLogger()


class YoukuSpider(scrapy.Spider):
    id = 0
    name = "youku"
    allowed_domains = ["youku.com"]
    start_urls = [
        "http://www.youku.com/",
    ]
    
    def __init__(self):
        pass

    def parse(self, response):
        for sel in response.xpath(
            '//div[@class="v v-large focusVideo ishover"]'
            '| //div[@class="v ishover"]'):
            log.debug('sel:%s' %(sel))
            item = items.YoukuItem()
            # get title, filter invalid item
            item['title'] = sel.xpath(
                'div[@class="v-link"]'
                '/a'
                '/@title[1]').extract()

            # get href, filter invalid item
            item['href'] = sel.xpath(
                'div[@class="v-link"]'
                '/a'
                '/@href[1]').extract()

            # get image_urls, filter invalid item
            item['image_urls'] = sel.xpath(
                'div[@class="v-thumb"]'
                '/img'
                '/@_src[1]').extract()
            # no _src, then get src
            if not item['image_urls']:
                item['image_urls'] = sel.xpath(
                    'div[@class="v-thumb"]'
                    '/img'
                    '/@src[1]').extract()

            YoukuSpider.id = add(YoukuSpider.id)
            item['id'] = YoukuSpider.id
            log.info('iid:%d,\nsel:%s,\nitem:%s'
                         %(YoukuSpider.id, sel, item))
            yield item