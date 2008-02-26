# -*- encoding:utf-8 -*-

import httplib,urlparse
import time
import oauth

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

HOST = 'http://api.douban.com'
REQUEST_TOKEN_URL = HOST+'/auth/request_token'
ACCESS_TOKEN_URL = HOST+'/auth/access_token'
AUTHORIZATION_URL = HOST+'/auth/authorize'

class OAuthClient:
    def __init__(self, server, key=None, secret=None):
        self.server = server
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.token = None

    def login(self, key=None, secret=None):
        if key and secret:
            self.token = oauth.OAuthToken(key, secret)
            return True
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                http_url=REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, None)
        token = self.fetch_token(oauth_request)

        self.authorize_token(token)
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=token, http_url=ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, token)
        self.token = self.fetch_token(oauth_request)
        #print 'Got access token:'
        #print self.token.key, self.token.secret
        return True

    def fetch_token(self, oauth_request):
        connection = httplib.HTTPConnection("%s:%d" % (self.server, 80))
        connection.request('GET', oauth_request.http_url, 
            headers=oauth_request.to_header()) 
        response = connection.getresponse()
        r = response.read()
        try:
            return oauth.OAuthToken.from_string(r)
        except:
            print r
            raise

    def authorize_token(self, token):
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, 
                http_url=AUTHORIZATION_URL)
        print 'please paste the url in your webbrowser, complete the authorization then come back:'
        print oauth_request.to_url()
        line = raw_input()
        print 'authorization was completed, press ANY KEY to continue'
 
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
    client.login(key='47c28e8f69497a61d747abae3bdc6f23',secret='231603d673b4e5c5')
    res = client.access_resource('GET', 'http://api.douban.com/test?a=b&c=d').read()
    print res
    assert res == 'OK'

if __name__ == '__main__':
    test()