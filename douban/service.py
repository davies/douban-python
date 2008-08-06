# encoding: UTF-8

import atom
import gdata.service
import douban
import urllib
import oauth, client

class DoubanService(gdata.service.GDataService):
    def __init__(self, api_key=None, secret=None,
            source='douban-python', server='api.douban.com', 
            additional_headers=None):
        self.api_key = api_key
        self.client = client.OAuthClient(key=api_key, secret=secret)
        gdata.service.GDataService.__init__(self, service='douban', source=source,
                server=server, additional_headers=additional_headers)

    def GetAuthorizationURL(self, callback=None):
        return self.client.get_authorization_url(callback)

    def ProgrammaticLogin(self, token_key=None, token_secret=None):
        return self.client.login(token_key, token_secret)

    def Get(self, uri, extra_headers={}, *args, **kwargs):
        auth_header = self.client.get_auth_header('GET', uri)
        if auth_header:
            extra_headers.update(auth_header)
        elif self.api_key:
            param = urllib.urlencode([('apikey', self.api_key)])
            if '?' in uri:
                uri += '&' + param
            else:
                uri += '?' + param
        return gdata.service.GDataService.Get(self, uri, extra_headers, *args, **kwargs)

    def Post(self, data, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('POST', uri, url_params))
        return gdata.service.GDataService.Post(self, data, uri, 
                extra_headers, url_params, *args, **kwargs)
    
    def Put(self, data, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('PUT', uri, url_params))
        return gdata.service.GDataService.Put(self, data, uri, 
                extra_headers, url_params, *args, **kwargs)

    def Delete(self, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('DELETE', uri, url_params))
        return gdata.service.GDataService.Delete(self, uri, extra_headers, url_params, *args, **kwargs)

    def GetPeople(self, uri):
        return self.Get(uri, converter=douban.PeopleEntryFromString)

    def GetPeopleFeed(self, uri):
        return self.Get(uri, converter=douban.PeopleFeedFromString)

    def SearchPeople(self, text_query, start_index=None, max_results=None):
        query = Query('/people/', text_query, start_index=start_index,
                max_results=max_results)
        return self.GetPeopleFeed(query.ToUri())
    
    def GetFriends(self, uri):
	return self.Get(uri, converter=douban.PeopleFeedFromString)

    def GetContacts(self, uri):
    	return self.Get(uri, converter=douban.PeopleFeedFromString)

    def GetAuthorizedUID(self, uri):
	return self.Get(urllib.quote(uri), converter=douban.PeopleEntryFromString)

    def GetBook(self, uri):
        return self.Get(uri, converter=douban.BookEntryFromString)

    def GetBookFeed(self, uri):
        return self.Get(uri, converter=douban.BookFeedFromString)

    def SearchBook(self, text_query, start_index=None, max_results=None):
        query = Query('/book/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetBookFeed(query.ToUri())

    def QueryBookByTag(self, tag, start_index=None, max_results=None):
        query = Query('/book/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetBookFeed(query.ToUri())

    def GetMovie(self, uri):
        return self.Get(uri, converter=douban.MovieEntryFromString)

    def GetMovieFeed(self, uri):
        return self.Get(uri, converter=douban.MovieFeedFromString)

    def SearchMovie(self, text_query, start_index=None, max_results=None):
        query = Query('/movie/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetMovieFeed(query.ToUri())

    def QueryMovieByTag(self, tag, start_index=None, max_results=None):
        query = Query('/movie/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetMovieFeed(query.ToUri())

    def GetMusic(self, uri):
        return self.Get(uri, converter=douban.MusicEntryFromString)

    def GetMusicFeed(self, uri):
        return self.Get(uri, converter=douban.MusicFeedFromString)

    def SearchMusic(self, text_query, start_index=None, max_results=None):
        query = Query('/music/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetMusicFeed(query.ToUri())

    def QueryMusicByTag(self, tag, start_index=None, max_results=None):
        query = Query('/music/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetMusicFeed(query.ToUri())

    def GetReview(self, uri):
        return self.Get(uri, converter=douban.ReviewEntryFromString)

    def GetReviewFeed(self, uri, orderby = 'score'):
	query = Query(uri, text_query=None, 
		start_index=None, max_results=None, orderby=orderby)
        return self.Get(query.ToUri(), converter=douban.ReviewFeedFromString)

    def CreateReview(self, title, content, subject, rating=None):
        subject = douban.Subject(atom_id=subject.id)
        entry = douban.ReviewEntry(subject=subject)
        if rating:
            entry.rating = douban.Rating(value=rating)
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        return self.Post(entry, '/reviews', 
                converter=douban.ReviewEntryFromString)
        
    def UpdateReview(self, entry, title, content, rating=None):
        if isinstance(entry,(str,unicode)):
            entry = self.Get(entry, douban.ReviewEntryFromString)
            
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        if rating:
             entry.rating = douban.Rating(value=rating)
        
        uri = entry.GetSelfLink().href  
        return self.Put(entry, uri, converter=douban.ReviewEntryFromString)
        
    def DeleteReview(self, entry):
        uri = entry.GetSelfLink().href  
        return self.Delete(uri)
        
    def GetCollection(self, uri):
        return self.Get(uri, converter=douban.CollectionEntryFromString)
        
    def GetCollectionFeed(self, uri):
        return self.Get(uri, converter=douban.CollectionFeedFromString)

    def GetMyCollection(self):
        return self.Get(urllib.quote('/people/@me/collection'), 
            converter=douban.CollectionFeedFromString)

    def AddCollection(self, status, subject, rating=None, tag=[], private=False):
        subject = douban.Subject(atom_id=subject.id)
        entry = douban.CollectionEntry(subject=subject,
                status=douban.Status(status))
        if rating:
            entry.rating = douban.Rating(rating)
        if isinstance(tag, (str,unicode)):
            tag = filter(None, tag.split(' '))
        entry.tags = [douban.Tag(name=t) for t in tag]
        
        return self.Post(entry, '/collection', 
                converter=douban.CollectionEntryFromString)

    def UpdateCollection(self, entry, status, tag=[], rating=None, private=False):
        if isinstance(entry,(str,unicode)):
            entry = self.Get(entry, douban.CollectionEntryFromString)
        
        entry.status = douban.Status(status)
        if rating:
             entry.rating = douban.Rating(rating)
        if tag:
            if isinstance(tag, (str,unicode)):
                tag = filter(None, tag.split(' '))
            entry.tags = [douban.Tag(name=t) for t in tag]
        else:
            entry.tags = [douban.Tag(name=t.name) for t in entry.tags]
        
        uri = entry.GetSelfLink().href  
        return self.Put(entry, uri, converter=douban.CollectionEntryFromString)
    
    def DeleteCollection(self, entry):
        uri = entry.GetSelfLink().href  
        return self.Delete(uri)

    def GetTagFeed(self, uri):
        return self.Get(uri, converter=douban.TagFeedFromString)


class Query(gdata.service.Query):
    def __init__(self, feed=None, text_query=None, start_index=None,
            max_results=None, **params):
        gdata.service.Query.__init__(self, feed=feed, text_query=text_query,
                params=params)
        if start_index is not None:
            self.start_index = start_index
        if max_results is not None:
            self.max_results = max_results
