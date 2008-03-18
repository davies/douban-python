# -*- encoding:utf-8 -*-

import httplib,urlparse,cgi
import time
import oauth

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

HOST = 'http://api.douban.com'
REQUEST_TOKEN_URL = HOST+'/auth/request_token'
ACCESS_TOKEN_URL = HOST+'/auth/access_token'
AUTHORIZATION_URL = 'http://frodo.douban.com/service/api/auth/authorize'

class OAuthClient:
    def __init__(self, server, key=None, secret=None):
        self.server = server
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.token = None
        self.user_id = None

    def login(self, key=None, secret=None):
        if key and secret:
            self.token = oauth.OAuthToken(key, secret)
            return True
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                http_url=REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, None)
        token,_ = self.fetch_token(oauth_request)

        self.authorize_token(token)
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=token, http_url=ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, token)
        self.token, self.user_id = self.fetch_token(oauth_request)
        print self.token, self.user_id
        return self.token is not None

    def fetch_token(self, oauth_request):
        connection = httplib.HTTPConnection("%s:%d" % (self.server, 80))
        connection.request('GET', oauth_request.http_url, 
            headers=oauth_request.to_header()) 
        response = connection.getresponse()
        r = response.read()
        try:
            token = oauth.OAuthToken.from_string(r)
            params = cgi.parse_qs(r, keep_blank_values=False)
            user_id = params.get('douban_user_id')
            user_id = user_id and user_id[0]
            return token, user_id
        except:
            return None,None

    def authorize_token(self, token):
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, 
                http_url=AUTHORIZATION_URL)
        print 'please paste the url in your webbrowser, complete the authorization then come back:'
        print oauth_request.to_url()
        line = raw_input()
 
    def get_auth_header(self, method, uri, parameter={}):
        if not uri.startswith(HOST):
            uri = HOST + uri
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=self.token, http_method=method, http_url=uri, parameters=parameter)
        oauth_request.sign_request(signature_method, self.consumer, self.token)
        return oauth_request.to_header()
 
    def access_resource(self, method, url, body=None):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=self.token, http_url=url)
        oauth_request.sign_request(signature_method, self.consumer, self.token)
        headers = oauth_request.to_header()
        if method in ('POST','PUT'):
            headers['Content-Type'] = 'application/atom+xml; charset=utf-8'
        connection = httplib.HTTPConnection("%s:%d" % (self.server, 80))
        connection.request(method, url, body=body,
            headers=headers)
        return connection.getresponse()

def test():
    client = OAuthClient('api.douban.com', 
            key='7f1494926beb1d527d3dbdb743c157f6',
            secret='50cd7b45a6859b36')
    client.login()
    res = client.access_resource('GET', 'http://api.douban.com/test?a=b&c=d').read()
    print res

if __name__ == '__main__':
    test()