#!/usr/bin/python
#coding:utf-8

import os
import web


urls = (
    r'/', 'index',
    r'/page/(\d+)', 'index'
    )


add = lambda x: x + 1


class index(object):

    def __init__(self):
        self.db = web.database(
            dbn='mysql',
            host='127.0.0.1',
            port=3306,
            db='test',
            user='root',
            pw='kongdeyu')
        self.render = web.template.render('templates' + os.sep)

    def __del__(self):
        pass

    def GET(self, page=1):
        page = int(page)
        perpage = 10
        offset = (page - 1) * perpage
        posts = self.db.select('tbl', offset=offset, limit=perpage)
        postcount = self.db.query('select count(*) as count from tbl')[0]
        pages = postcount.count / perpage

        # boundary revision
        if postcount.count % perpage > 0:
            pages = add(pages)

        # out of boundary
        if page > pages:
            raise web.seeother('/')
        else:
            return self.render.index(posts=posts, pages=pages)


class Error(Exception):
    pass


def main():
    app = web.application(urls, globals())
    app.run()


if '__main__' == __name__:
    main()
