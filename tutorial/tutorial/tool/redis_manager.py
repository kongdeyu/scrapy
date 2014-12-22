#!/usr/bin/python
#coding:utf-8

import redis


class RedisManager(object):

    def __init__(
        self,
        host,
        port,
        db=0,
        password=None,
        socket_timeout=None,
        encoding='utf-8',
        encoding_errors='strict'):
        try:
            self.conn_pool = redis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=password,
                socket_timeout=socket_timeout,
                encoding=encoding,
                encoding_errors=encoding_errors)
            self.conn = redis.StrictRedis(
                connection_pool=self.conn_pool)
        except Exception as e:
            self.conn_pool.disconnect()
            raise Error(e)
            
    def __del__(self):
        try:
            self.conn_pool.disconnect()
        except Exception as e:
            raise Error(e)

    def hset(self, name, key, value):
        try:
            if 1 == self.conn.hset(name, key, value):
                return True
            else:
                return False
        except Exception as e:
            raise Error(e)

    def hexists(self, name, key):
        try:
            return self.conn.hexists(name, key)
        except Exception as e:
            raise Error(e)


class Error(Exception):
    pass