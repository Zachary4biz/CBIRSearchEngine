# encoding=utf-8
import web
import ColorDescriptor
import IndexImage
import Searcher

urls = (
    '/searchengine','searchengine',
)

render = web.template.render('templates/')

class searchengine(object):
    def GET(self):
        return render.searchengine()

    # def POST(self):
