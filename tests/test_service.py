# encoding: UTF-8

import douban.service

SERVER='api.douban.com'
# for user apitest
API_KEY='b15d572d2689de5014180587739d9af0'
SECRET='20d35fcbd52445d1'
TOKEN_KEY='37b6cf391d702a4aa7246dab58507ede'
TOKEN_SECRET='c22ecfea3ec593a8'

class TestDoubanService:
    def __init__(self):
        self.client = douban.service.DoubanService(server=SERVER,
                    api_key=API_KEY,secret=SECRET)
        self.client.ProgrammaticLogin(token_key=TOKEN_KEY,token_secret=TOKEN_SECRET)
    
    def setUp(self):
        pass

    def test_people(self):
        people = self.client.GetPeople('/people/1000001')
        assert people.title.text == "阿北"
        assert people.location.text == "北京"
        assert people.GetSelfLink().href == "http://api.douban.com/people/1000001"
        assert people.GetAlternateLink().href == "http://www.douban.com/people/ahbei/"

    def test_search_people(self):
        feed = self.client.SearchPeople("阿北")
        assert any( e.title.text == "阿北" for e in feed.entry)

    def test_query_book_by_tag(self):
        feed = self.client.QueryBookByTag("小说")
        assert len(feed.entry)

    def test_get_tag_feed(self):
        uri = '/book/subject/1000001/tags'
        feed = self.client.GetTagFeed(uri)
        assert any(e.title.text == "第一" for e in feed.entry)

     
    def test_get_book(self):
        uri = '/book/subject/1489401'
        entry = self.client.GetBook(uri)
        assert entry.title.text == '安徒生童话(永远的珍藏)'
        assert entry.GetAlternateLink().href == "http://www.douban.com/subject/1489401/"
        assert any(att.name == 'isbn10' for att in entry.attribute)
        assert any(att.name == 'isbn13' for att in entry.attribute)
        assert any(att.name == 'translator' for att in entry.attribute)
        assert any(att.text == '叶君健' for att in entry.attribute)
        assert any(att.text == '平装' for att in entry.attribute)
        assert entry.rating.min == '1'
        assert entry.rating.max == '5'
        #assert entry.rating.average == '4.71'



    def test_collection(self):
        book_uri = '/book/subject/1489401'
        subject = self.client.GetBook(book_uri)

        assert subject.tag[0].name == '童话'
        
        entry = self.client.AddCollection('wish', subject, tag=['nice', '安徒生'])
        assert entry.status.text == 'wish'
        assert len(entry.tags) == 2
        assert entry.tags[0].name == 'nice'
        assert entry.tags[1].name == '安徒生'
        
        entry = self.client.GetCollection(entry.GetSelfLink().href)
        print entry

        assert entry.status.text == 'wish'
        assert len(entry.tags) == 2
        assert entry.tags[0].name == 'nice'
        
        #entry = self.client.UpdateCollection(entry, 'read', ['gnice', '安徒生', '童话'], rating=3)
        entry = self.client.UpdateCollection(entry, 'read', rating=3)
        assert entry.status.text == 'read'
        assert entry.rating.value == '3'
        assert entry.tags[0].name == 'nice'
        assert entry.tags[1].name == '安徒生'
        

        assert self.client.DeleteCollection(entry)

    def test_review(self):
        book_uri = '/book/subject/1489401'
        subject = self.client.GetBook(book_uri)
        
        entry = self.client.CreateReview('good', 'very good '*105, subject, 4)

        assert entry.title.text == 'good'
        assert entry.rating.value == '4'
        self.client.DeleteReview(entry)

 
