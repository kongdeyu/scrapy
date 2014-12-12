#coding:utf-8

import os
import web

urls = (
    '/', 'index',
    '/page/(\d+)', 'index'
    )

class index:
    def GET(self, page = 1):
        db = web.database(dbn = 'mysql',
                          host = '127.0.0.1',
                          port = 3306,
                          db = 'test',
                          user = 'root',
                          pw = 'kongdeyu')
        page = int(page)
        perpage = 10
        offset = (page - 1) * perpage
        posts = db.select('tbl', offset = offset, limit = perpage)
        postcount = db.query('select count(*) as count from tbl')[0]
        pages = postcount.count / perpage
        if postcount.count % perpage > 0:
            pages += 1
        if page > pages:
            raise web.seeother('/')
        else:
            render = web.template.render('templates' + os.sep)
            return render.index(posts = posts, pages = pages)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()