# -*- encoding:utf-8 -*-

import httplib
import time
import oauth

signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
#signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

class OAuthClient:
    REQUEST_TOKEN_URL = '/auth/request_token'
    ACCESS_TOKEN_URL = '/auth/access_token'
    AUTHORIZATION_URL = 'http://frodo.douban.com/service/api/auth/authorize'

    def __init__(self, server, key=None, secret=None):
        self.server = server
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.token = None

    def login(self, key=None, secret=None):
        if key and secret:
            self.token = oauth.OAuthToken(key, secret)
            return True
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, None)
        token = self.fetch_token(oauth_request)

        self.authorize_token(token)
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=token, http_url=self.ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, token)
        self.token = self.fetch_token(oauth_request)
        print 'Got access token:'
        print self.token.key, self.token.secret
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
                http_url=self.AUTHORIZATION_URL)
        print 'please paste the url in your webbrowser, complete the authorization then come back:'
        print oauth_request.to_url()
        line = raw_input()
        print 'authorization was completed, continue'
 
    def get_auth_token(self, method=None, uri=None):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=self.token, http_url=uri)
        oauth_request.sign_request(signature_method, self.consumer, self.token)
        return oauth_request.to_header()['Authorization']
 
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
    res = client.access_resource('GET', '/test').read()
    assert res == 'OK'

if __name__ == '__main__':
    test()