#!/usr/bin/python
#coding:utf-8

import MySQLdb

class DBManager:
    def __init__(self,
                 dbhost,
                 dbport,
                 dbusername,
                 dbpasswd,
                 dbname,
                 dbcharset):
        try:
            self.conn = MySQLdb.connect(host = dbhost,
                                        port = dbport,
                                        user = dbusername,
                                        passwd = dbpasswd,
                                        db = dbname,
                                        charset = dbcharset)
        except Exception as e:
            self.conn.close()
            raise Error(e)
            
    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            raise Error(e)

    @staticmethod
    def escape_string(cnt):
        try:
            return MySQLdb.escape_string(cnt)
        except Exception as e:
            raise Error(e)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def execute(self, sql, is_commit = True):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            if (is_commit == True):
                self.commit()
        except Exception as e:
            self.rollback()
            raise Error(e)
        finally:
            cursor.close()

    def insert(self, sql, is_commit = True):
        self.execute(sql, is_commit)

    def delete(self, sql, is_commit = True):
        self.execute(sql, is_commit)

    def fetch_list(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise Error(e)
        finally:
            cursor.close()

    def fetch_dict(self, sql):
        try:
            cursor = self.conn.cursor(
                cursorclass = MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise Error(e)
        finally:
            cursor.close()

class Error(Exception):
    pass