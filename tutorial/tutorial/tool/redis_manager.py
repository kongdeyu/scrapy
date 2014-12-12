#!/usr/bin/python
#coding:utf-8

import redis

class RedisManager:
    def __init__(self,
                 rhost,
                 rport,
                 rdb = 0,
                 rpassword = None,
                 rsocket_timeout = None,
                 rcharset = 'utf-8',
                 rerrors = 'strict',
                 runix_socket_path = None):
        try:
            self.conn_pool = redis.ConnectionPool(host = rhost,
                                        port = rport,
                                        db = rdb,
                                        password = rpassword,
                                        socket_timeout = rsocket_timeout,
                                        encoding = rcharset,
                                        encoding_errors = rerrors)
            self.conn = redis.StrictRedis(
                                        connection_pool = self.conn_pool)
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