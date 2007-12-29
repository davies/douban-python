# encoding: UTF-8

import douban.service

class TestDoubanService:
    def setUp(self):
        self.client = douban.service.DoubanService()

    def test_people(self):
        people = self.client.GetPeople('http://api.douban.com/people/1000001')
        assert people.title.text == "阿北"

    def test_search_people(self):
        feed = self.client.SearchPeople("阿北")
        found = False
        for entry in feed.entry:
            if entry.title.text == "阿北":
                found = True
                break
        assert found

    def test_query_book_by_tag(self):
        feed = self.client.QueryBookByTag("小说")
        assert len(feed.entry)

    def test_get_tag_feed(self):
        uri = 'http://api.douban.com/book/subject/1000001/tags'
        feed = self.client.GetTagFeed(uri)
        assert any(e.title.text == "第一" for e in feed.entry)
