# encoding: UTF-8

import douban.service

SERVER='api.douban.com'
API_KEY='7f1494926beb1d527d3dbdb743c157f6'
SECRET='50cd7b45a6859b36'
TOKEN_KEY='47c28e8f69497a61d747abae3bdc6f23'
TOKEN_SECRET='231603d673b4e5c5'
PREFIX=''

class TestDoubanService:
    def __init__(self):
        self.client = douban.service.DoubanService(server=SERVER,
                    api_key=API_KEY,secret=SECRET)
        self.client.ClientLogin(token_key=TOKEN_KEY,token_secret=TOKEN_SECRET)
    
    def setUp(self):
        pass

    def test_people(self):
        people = self.client.GetPeople(PREFIX+'/people/1000001')
        assert people.title.text == "阿北"

    def test_search_people(self):
        feed = self.client.SearchPeople("阿北")
        assert any( e.title.text == "阿北" for e in feed.entry)

    def test_query_book_by_tag(self):
        feed = self.client.QueryBookByTag("小说")
        assert len(feed.entry)

    def test_get_tag_feed(self):
        uri = PREFIX+'/book/subject/1000001/tags'
        feed = self.client.GetTagFeed(uri)
        assert any(e.title.text == "第一" for e in feed.entry)

    def test_get_book(self):
        uri = PREFIX+'/book/subject/1489401'
        entry = self.client.GetBook(uri)
        assert entry.title.text == '安徒生童话'

    def test_login(self):
        uri = PREFIX+'/test'
        r = self.client.Get(uri, converter=str)
        assert r == 'OK'

    def test_review(self):
        book_uri = PREFIX+'/book/subject/1489401'
        subject = self.client.GetBook(book_uri)
        
        entry = self.client.CreateReview('good', 'Very Good'*5, subject, 4)
        assert entry.title.text == 'good'
        assert entry.rating.value == '4'
        
        entry = self.client.GetReview(entry.GetSelfLink().href)
        assert entry.title.text == 'good'
        assert entry.rating.value == '4'
        
        feed_uri = PREFIX+'/people/davies/reviews'
        feed = self.client.GetReviewFeed(feed_uri)
        n = int(feed.total_results.text)
        assert n >= 1
        
        entry = self.client.UpdateReview(entry, 'good2', 'Very Nice'*5, 5)
        print entry.title.text
        assert entry.title.text == 'good2'
        assert entry.rating.value == '5'
        
        assert self.client.DeleteReview(feed.entry[1])
        feed = self.client.GetReviewFeed(feed_uri)
        assert n-1 == int(feed.total_results.text)
        
        
    def test_collection(self):
        book_uri = PREFIX+'/book/subject/1489401'
        subject = self.client.GetBook(book_uri)
        
        entry = self.client.AddCollection('wish', subject, tag='nice')
        assert entry.status.text == 'wish'
        assert len(entry.tags) == 1
        assert entry.tags[0].name == 'nice'
        
        entry = self.client.GetCollection(entry.GetSelfLink().href)
        assert entry.status.text == 'wish'
        assert len(entry.tags) == 1
        assert entry.tags[0].name == 'nice'
        
        entry = self.client.UpdateCollection(entry, 'read', rating=3)
        assert entry.status.text == 'read'
        assert entry.rating.value == '3'
        assert entry.tags[0].name == 'nice'

        assert self.client.DeleteCollection(entry)