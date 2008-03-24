# -*- encoding:utf-8 -*-

import httplib,urlparse,cgi
import time
import oauth

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

API_HOST = 'http://api.douban.com'
AUTH_HOST = 'http://frodo.douban.com'
REQUEST_TOKEN_URL = AUTH_HOST+'/service/auth/request_token'
ACCESS_TOKEN_URL = AUTH_HOST+'/service/auth/access_token'
AUTHORIZATION_URL = AUTH_HOST+'/service/auth/authorize'

class OAuthClient:
    def __init__(self, server='frodo.douban.com', key=None, secret=None):
        self.server = server
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.token = None
        self.user_id = None

    def login(self, key=None, secret=None):
        if key and secret:
            self.token = oauth.OAuthToken(key, secret)
            return True

        key,secret = self.get_request_token()
        url = self.get_authorization_url(key, secret)
        print 'please paste the url in your webbrowser, complete the authorization then come back:'
        print url
        line = raw_input()
        
        key, secret = self.get_access_token(key, secret)
        return self.login(key, secret)

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
            print r
            raise Exception,str(r)
            return None,None

    def get_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                        http_url=REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, None)
        token,_ = self.fetch_token(oauth_request)
        return token.key, token.secret

    def get_authorization_url(self, key, secret, callback=None):
        token = oauth.OAuthToken(key, secret)
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, 
                http_url=AUTHORIZATION_URL, callback=callback)
        return oauth_request.to_url()
 
    def get_access_token(self, key=None, secret=None, token=None):
        if key and secret:
            token = oauth.OAuthToken(key, secret)
        assert token is not None
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=token, http_url=ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, token)
        token, user_id = self.fetch_token(oauth_request)
        if token:
            return token.key, token.secret
 
    def get_auth_header(self, method, uri, parameter={}):
        if not uri.startswith('http'):
            uri = API_HOST + uri
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
