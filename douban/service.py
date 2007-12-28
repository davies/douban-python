# encoding: UTF-8

import gdata.service
import douban

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

    def GetBook(self, uri):
        return self.Get(uri, converter=douban.BookEntryFromString)

    def GetBookFeed(self, uri):
        return self.Get(uri, converter=douban.BookFeedFromString)

    def GetMovie(self, uri):
        return self.Get(uri, converter=douban.MovieEntryFromString)

    def GetMovieFeed(self, uri):
        return self.Get(uri, converter=douban.MovieFeedFromString)

    def GetMusic(self, uri):
        return self.Get(uri, converter=douban.MusicEntryFromString)

    def GetMusicFeed(self, uri):
        return self.Get(uri, converter=douban.MusicFeedFromString)

    def GetReview(self, uri):
        return self.Get(uri, converter=douban.ReviewEntryFromString)

    def GetReviewFeed(self, uri):
        return self.Get(uri, converter=douban.ReviewFeedFromString)

    def GetCollectionFeed(self, uri):
        return self.Get(uri, converter=douban.CollectionFeedFromString)

    def GetTagFeed(self, uri):
        return self.Get(uri, converter=douban.TagFeedFromString)
