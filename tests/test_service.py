# encoding: UTF-8

import douban.service
import urllib
import atom
import douban

SERVER='api.douban.com'
# for user apitest

API_KEY=''
SECRET=''
TOKEN_KEY=''
TOKEN_SECRET=''
class TestDoubanService:
    def __init__(self):
        self.client = douban.service.DoubanService(server=SERVER,
                    api_key=API_KEY,secret=SECRET)
        self.client.ProgrammaticLogin(token_key=TOKEN_KEY,token_secret=TOKEN_SECRET)
    
    def setUp(self):
        pass

    def test_people(self):
        people = self.client.GetPeople('/people/1000001')
	assert people.uid.text == 'ahbei'
        assert people.title.text == "阿北"
        assert people.location.text == "北京"
        assert people.GetSelfLink().href == "http://api.douban.com/people/1000001"
        assert people.GetAlternateLink().href == "http://www.douban.com/people/ahbei/"

    def test_search_people(self):
        feed = self.client.SearchPeople("阿北")
        assert any( e.title.text == "阿北" for e in feed.entry)

    def test_authorized_UID(self):
	people = self.client.GetAuthorizedUID('/people/@me')
	assert people.uid.text == '2463802'
    
    def test_get_friends(self):
	feed = self.client.GetFriends('/people/2463802/friends')
	assert any( e.uid.text == 'jili8' for e in feed.entry)
    
    def test_get_contacts(self):
	feed = self.client.GetFriends('/people/2463802/contacts')
	assert any( e.uid.text == 'youha' for e in feed.entry)
    
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

        entry = self.client.AddCollection('wish', subject, tag=['read', '安徒生'], private=True)
        assert entry.status.text == 'wish'
        assert len(entry.tags) == 2
        assert entry.tags[0].name == 'read'
        assert entry.tags[1].name == '安徒生'
        entry = self.client.GetCollection(entry.GetSelfLink().href)
	assert entry.status.text == 'wish'
        assert len(entry.tags) == 2
        entry = self.client.UpdateCollection(entry, 'read', ['read', '安徒生', '童话'], rating=3, private=True)
        assert entry.status.text == 'read'
        assert entry.rating.value == '3'
        assert entry.tags[0].name == 'read'
        assert entry.tags[1].name == '安徒生'
        assert self.client.DeleteCollection(entry)

	feed = self.client.GetMyCollection('/people/2463802/collection', 'book', 'read', 'wish', '1', '3', '2008-12-28T21:47:00+08:00', '2007-12-28T21:47:00+08:00')
	assert len(feed.entry)

    def test_review(self):
        book_uri = '/book/subject/1489401'
        subject = self.client.GetBook(book_uri)
        
        entry = self.client.CreateReview('good', 'very good '*105, subject, 4)

        assert entry.title.text == 'good'
        assert entry.rating.value == '4'
	feed = self.client.GetReviewFeed('/book/subject/1489401/reviews', orderby='score')
	assert any(entry.title.text == 'good' for entry in feed.entry)
        self.client.DeleteReview(entry)
    
    def test_broadcasting(self):
	uri = '/people/sakinijino/miniblog'
	broadcastingfeed = self.client.GetBroadcastingFeed(uri, 1, 2)
	entry = broadcastingfeed.entry[0];
	#assert any(cate.term == "http://www.douban.com/2007#miniblog.blog" for cate in entry.category)

	contacturi = '/people/2463802/miniblog/contacts'
	broadcastingfeed = self.client.GetContactsBroadcastingFeed(contacturi, 1, 2)
	entry = broadcastingfeed.entry[0]
	#assert any(cate.term == "http://www.douban.com/2007#miniblog.saying" for cate in entry.category)
 	entry = douban.BroadcastingEntry()
	entry.content = atom.Content(text = "You should not see this")
	entry = self.client.AddBroadcasting("/miniblog/saying", entry)
	self.client.DeleteBroadcasting(entry)
  
    def test_note(self):
	uri = '/note/17030527'
	entry = self.client.GetNote(uri)
	assert entry.content.text == 'my note'
	assert entry.title.text == 'my note'
	entry = douban.NoteEntry()
	entry.title = atom.Title(text="a test note")
        entry.content = atom.Content(text="this note is for testing") 
	entry = self.client.AddNote("/notes", entry, False, True)
	assert entry.title.text == 'a test note'
        entry = self.client.UpdateNote(entry, 'it a good day!', 'my good note', True, False);
	assert entry.title.text == 'my good note'
	self.client.DeleteNote(entry)
	
      	feed = self.client.GetMyNotes('/people/2463802/notes', 1, 2)
	assert any(entry.title.text == 'a test note' for entry in feed.entry)
