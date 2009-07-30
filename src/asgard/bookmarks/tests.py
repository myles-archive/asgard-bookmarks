import unittest, datetime

from django.test import Client
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse

from asgard.bookmarks.models import Bookmark
from tagging.models import Tag

class BookmarkTestCase(unittest.TestCase):
	def setUp(self):
		self.bookmark = Bookmark()
		self.bookmark.title = 'Myles Braithwaite'
		self.bookmark.url = 'http://mylesbraithwaite.com/'
		self.bookmark.tags = 'myles braithwaite'
		self.bookmark.published = datetime.datetime.now()
		self.bookmark.save()
		self.site = Site(id=settings.SITE_ID, domain="example.com", name="example.com").save()
		self.client = Client()
	
	def tearDown(self):
		self.bookmark.delete()
	
	def testBookmarkUUID(self):
		self.assertEquals(self.bookmark.uuid, 'c236fffb-49ee-3ddf-8f2b-0c061951d113')
	
	def testBookmarkIndex(self):
		response = self.client.get(reverse('bookmark_index'))
		self.assertEquals(response.status_code, 200)
	
	def testBookmarkDetailThoughModel(self):
		response = self.client.get(self.bookmark.get_internal_url())
		self.assertEquals(response.status_code, 200)
	
	def testBookmarkDetailThoughURL(self):
		response = self.client.get(reverse('bookmark_detail', args=[self.bookmark.uuid,]))
		self.assertEquals(response.status_code, 200)
	
	def testTagList(self):
		response = self.client.get(reverse('bookmark_tag_list'))
		self.assertEquals(response.status_code, 200)
	
	def testTagDetail(self):
		tag = Tag.objects.get_for_object(self.bookmark)[0]
		response = self.client.get(reverse('bookmark_tag_detail', args=[tag.name,]))
		self.assertEquals(response.status_code, 200)
