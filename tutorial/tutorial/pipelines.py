# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import logging
import os
import scrapy
import items
from tool import db_manager
from tool import redis_manager


log = logging.getLogger()


class TutorialPipeline(object):

    def __init__(self):
        # init redis
        try:
            self.redis = redis_manager.RedisManager(
                host='10.81.14.171',
                port=8888)
        except redis_manager.Error as e:
            log.critical('e:%s, connect to redis fail' %(e))
            exit()

        # init db
        try:
            self.db = db_manager.DBManager(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='kongdeyu',
                db='test',
                charset='utf8')
        except db_manager.Error as e:
            log.critical('e:%s, connect to db fail' %(e))
            exit()
        
    def process_item(self, item, spider):
        # filter invalid item
        if not item['title']:
            log.warning('iid:%d, no title' %(item['id']))
            raise scrapy.exceptions.DropItem('no title')
        if not item['href']:
            log.warning('iid:%d, no href' %(item['id']))
            raise scrapy.exceptions.DropItem('no href')
        if not item['images']:
            log.warning('iid:%d, no images' %(item['id']))
            raise scrapy.exceptions.DropItem('no images')

        title = item['title'][0].encode('utf-8')
        href = item['href'][0].encode('utf-8')
        images = item['images'][0]['url'].encode('utf-8')

        # filter repeated item
        if self.redis.hexists('hrefs', href):
            log.info('iid:%d, repeated item' %(item['id']))
            raise scrapy.exceptions.DropItem('repeated item')
        
        # insert hrefs to redis
        self.redis.hset('hrefs', href, 1)

        # valid item, insert to db
        try:
            sql = ('insert into tbl(title, href, img) values("%s", "%s", "%s");'
                      %(db_manager.DBManager.escape_string(title),
                      db_manager.DBManager.escape_string(href),
                      db_manager.DBManager.escape_string(images)))
            self.db.insert(sql)
            log.info('iid:%d, sql:%s, insert to db success'
                         %(item['id'], sql))
        except db_manager.Error as e:
            log.warning('iid:%d, sql:%s, e:%s, insert to db fail'
                                %(item['id'], sql, e))
        return item