#!/usr/bin/env python
#coding=utf-8

import sys

try:
    import web
    render = web.template.render('examples/templates/')
except Exception:
    print 'please install webpy first'
    sys.exit(0)

import douban.service
from douban.client import OAuthClient

API_KEY='7f1494926beb1d527d3dbdb743c157f6'
SECRET='50cd7b45a6859b36'

token = None
secret = None

request_tokens = {}
access_token = None

class index(object):
    def GET(self):
        print """<form action="/search" method="GET">
<input name="q" width="30" value="monty python">
<input type="submit" value="搜索电影">
</form>"""

        
class search(object):
    def GET(self):
        q = web.input().get('q','')
        client = douban.service.DoubanService(server=SERVER,
                    api_key=API_KEY,secret=SECRET)
        feed = client.SearchMovie(q)
        print "<html><body>"
        for movie in feed.entry:
            print '<a href="%s">%s</a>' % (movie.GetAlternateLink().href, movie.title.text)
            print '<a href="/collection?sid=%s">收藏</a>' % (movie.id.text)
            print '<br/>'
        print "</body></html>"

class collection(object):
    def GET(self):
        sid = web.input().get('sid','')
        if not sid:
            print 'no sid'
            return 
        key = web.input().get('token','')
        client = OAuthClient(SERVER, API_KEY, SECRET) 
        
        global access_token
        if not access_token and key in request_tokens:
            access_token = client.get_access_token(key, request_tokens[key])
            
        if access_token:
            service = douban.service.DoubanService(server=SERVER, api_key=API_KEY, secret=SECRET)
            key,secret = access_token
            if service.ProgrammaticLogin(key, secret):
                movie = service.GetMovie(sid)
                entry = service.AddCollection('wish', movie, tag=['test'])
                if entry:
                    print 'add to collection successfully'
                else:
                    print 'add to collection failed'
            else:
                print 'login failed'
        else:
            client = OAuthClient(SERVER, API_KEY, SECRET) 
            key, secret = client.get_request_token()
            request_tokens[key] = secret
            
            url = client.get_authorization_url(key, secret, 
                    callback='http://localhost:8080/collection?sid=%s&token=%s' %(sid,key))
            web.tempredirect(url)

urls = (
    '/', 'index',
    '/search', 'search',
    '/collection', 'collection',
)
    
if __name__ == '__main__':
    web.run(urls, globals())