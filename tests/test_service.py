# encoding: UTF-8

import douban.service

class TestDoubanService:
    def setUp(self):
        self.client = douban.service.DoubanService()

    def test_people(self):
        people = self.client.GetPeople('http://api.douban.com/people/1000001')
        assert people.title.text == "阿北"
