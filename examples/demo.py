#!/usr/bin/env python
#coding=utf-8

import sys

try:
    import web
except Exception:
    print 'please install webpy first'
    sys.exit(0)

try:
    from douban.service import DoubanService
    from douban.client import OAuthClient
except ImportError:
    print 'please install douban-python'
    sys.exit(0)

HOST = 'http://localhost:8080'
API_KEY='7f1494926beb1d527d3dbdb743c157f6'
SECRET='50cd7b45a6859b36'

token = None
secret = None

request_tokens = {}
access_token = None

def html_header():
    print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>API认证演示</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
    body {padding:0;margin: 0;background: #FEFEFE;}
    #maxw{ margin: 0 auto; padding:8px 30px;  background: #FFF;  max-width: 964px; width:expression( documentElement.clientWidth > 940 ? (documentElement.clientWidth == 0 ? (body.clientWidth >940 ? "940" : "auto") : "940px") : "auto" ); }

    form { padding: 0; border: 0px; }
    textarea{ overflow:auto; }
    a:link { color: #336699; text-decoration: none; }
    a:visited { color: #666699; text-decoration: none; }
    a:hover { color: #FFFFFF; text-decoration: none; background: #003399; }
    a:active { color: #FFFFFF; text-decoration: none; background: #FF9933; }
    a img { border-width:0; }

    body,td,th { font: 12px Arial, Helvetica, sans-serif; line-height: 150%; }
    table { border-collapse:collapse; border: none; padding: 0; margin: 0; }
    h1 { font-size: 25px; font-weight: bold; color: #494949; margin:0 0 0px 0; padding: 8px 0px 6px 0px; line-height:1.1em; }
    h2 { font: 14.8px normal Arial, Helvetica, sans-serif; color: #006600; margin-bottom: 5px; line-height: 150%; }
    h3 {width:100%;height:26px;margin-left:4px;font: 14.8px normal Arial, Helvetica, sans-serif;color: #666666;margin-bottom: 1px;line-height: 150%;background:url(/pics/topicbar.gif) no-repeat right top}
    h3 img{margin:1px 1px 0 0;}
    ul { list-style-type: none; margin: 0; padding: 0; }
    h4 {height:26px; margin:0 0 15px 4px; font: 12px normal Arial, Helvetica, sans-serif;color: #666666;line-height: 1.8em;background:url(/pics/topicbar.gif) no-repeat right top;}

    .obss {width :100%}
    .obs{ margin: 0 0 10px 0; float: left; text-align: center; overflow: hidden; width: 105px; }
    .obs dt{ height: 114px; width: 105px; overflow: hidden; }
    .obs dd{ margin: 0; height: 80px; overflow: hidden; }

    .gact { color: #BBBBBB; font-size: 12px; text-align: center; cursor:pointer; }
    </style>
    <body>
    <div id="maxw">
    <h1>API认证演示</h1>"""

def html_footer():
    print """
    </div>
    </body>
</html>"""

def search_panel(q = "monty python"):
    print """
            <h2>搜索电影并添加收藏...</h2>
            <form action="/search" method="GET">
            <input name="q" width="30" value="%s">
            <input type="submit" value="搜索电影">
            </form>""" % (q)

class index(object):
    def GET(self):
        html_header()
        search_panel()
        html_footer()

        
class search(object):
    def GET(self):
        q = web.input().get('q','')
        service = DoubanService(api_key=API_KEY,secret=SECRET)
        feed = service.SearchMovie(q)
        html_header()
        search_panel(q)
        print '<div class="obss" style="margin-top:20px">'
        for movie in feed.entry:
            print '<dl class="obs"><dt>'
            print '<div class="gact"><a href="/collection?sid=%s">想看</a></div>' % (movie.id.text)
            print '<a href="%s" title="%s"><img src="%s" class="m_sub_img"/></a>' % (movie.GetAlternateLink().href, movie.title.text, ((len(movie.link) >= 3) and movie.link[2].href) or '')
            print '</dt><dd>'
            print '<a href="%s">%s</a>' % (movie.GetAlternateLink().href, movie.title.text)
            print '</dd>'
            print '</dl>'
        print '</div>'
        html_footer()

class collection(object):
    def GET(self):
        sid = web.input().get('sid','')
        if not sid:
            print 'no sid'
            return 
        
        client = OAuthClient(key=API_KEY, secret=SECRET)

        global access_token
        if not access_token:
            key = web.input().get('oauth_token','')
            if key in request_tokens:
                try:
                    access_token = client.get_access_token(key, request_tokens[key])         
                except Exception:
                    access_token = None
                    print '获取用户授权失败'
                    return 
            else:
                client = OAuthClient(key=API_KEY, secret=SECRET) 
                key, secret = client.get_request_token()
                request_tokens[key] = secret
                url = client.get_authorization_url(key, secret, callback=HOST+'/collection?sid='+sid)
                web.tempredirect(url)
                return

        service = DoubanService(api_key=API_KEY, secret=SECRET)
        movie = service.GetMovie(sid)
        html_header()
        search_panel()
        print '<h2>你希望收藏电影: %s</h2>' % (movie.title.text)
        print '<div class="obss" style="margin-top:20px">'
        print '<dl class="obs"><dt>'
        print '<a href="%s" title="%s"><img src="%s" class="m_sub_img"/></a>' % (movie.GetAlternateLink().href, movie.title.text, movie.link[2].href)
        print '</dt><dd>'
        print '<a href="%s">%s</a>' % (movie.GetAlternateLink().href, movie.title.text)
        print '</dd>'
        print '</dl>'
        if access_token:
            key,secret = access_token
            if service.ProgrammaticLogin(key, secret):
                entry = service.AddCollection('wish', movie, tag=['test'])
                if entry:
                    print '<span>已添加到你的收藏</span>'
                else:
                    print '<span>添加收藏失败</span>'
        else:
            print '<span>添加收藏失败，可能你因为你没有授权这个应用访问你在豆瓣的数据</span>'
        print '</div>'
        html_footer()

urls = (
    '/', 'index',
    '/search', 'search',
    '/collection', 'collection',
)
    
if __name__ == '__main__':
    web.run(urls, globals())
