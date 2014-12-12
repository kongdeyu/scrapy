# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging
import json
import codecs
import items
import scrapy
from tool import db_manager

log = logging.getLogger()

class TutorialPipeline(object):
    def __init__(self):
        try:
            self.db = db_manager.DBManager(dbhost = '127.0.0.1',
                                            dbport = 3306,
                                            dbusername = 'root',
                                            dbpasswd = 'kongdeyu',
                                            dbname = 'test',
                                            dbcharset = 'utf8')
        except db_manager.Error as e:
            log.critical('e:%s, connect to db fail' %(e))
            exit()
        
    def process_item(self, item, spider):
        # filter invalid item
        if not item['title']:
            log.warning('item:%s, no title' %(title))
            raise items.YoukuItem('no title')
        if not item['href']:
            log.warning('item:%s, no href' %(title))
            raise items.YoukuItem('no href')
        if not item['images']:
            log.warning('item:%s, no images' %(title))
            raise items.YoukuItem('no images')

        # valid item, insert to db
        try:
            sql = 'insert into tbl(title, href, img) values("%s", "%s", "%s");'\
                        %(db_manager.DBManager.escape_string(
                            item['title'][0].encode('utf-8')),
                          db_manager.DBManager.escape_string(
                              item['href'][0].encode('utf-8')),
                          db_manager.DBManager.escape_string(
                              item['images'][0]['url'].encode('utf-8')))
            self.db.insert(sql)
            log.info('sql:%s, insert to db success' %(sql))
        except db_manager.Error as e:
            log.warning('sql:%s, e:%s, insert to db fail' %(sql, e))
        return item