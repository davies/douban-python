# encoding: UTF-8

import gdata.service
import douban
import urllib

class DoubanService(gdata.service.GDataService):
    def __init__(self, email=None, password=None, source=None,
            server='api.douban.com', api_key=None, additional_headers=None):
        gdata.service.GDataService.__init__(self, email=email,
                password=password, service='douban', source=source,
                server=server, additional_headers=additional_headers)
        self.api_key = api_key

    def GetPeople(self, uri):
        return self.Get(uri, converter=douban.PeopleEntryFromString)

    def GetPeopleFeed(self, uri):
        return self.Get(uri, converter=douban.PeopleFeedFromString)

    def SearchPeople(self, text_query, start_index=None, max_results=None):
        query = Query('/people', text_query, start_index=start_index,
                max_results=max_results)
        return self.GetPeopleFeed(query.ToUri())

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

    def GetReviewFeed(self, uri):
        return self.Get(uri, converter=douban.ReviewFeedFromString)

    def GetCollectionFeed(self, uri):
        return self.Get(uri, converter=douban.CollectionFeedFromString)

    def Get(self, uri, converter=None):
        if self.api_key:
            param = urllib.urlencode([('apikey', self.api_key)])
            if '?' in uri:
                uri += '&' + param
            else:
                uri += '?' + param
        return gdata.service.GDataService.Get(self, uri, converter=converter)

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
