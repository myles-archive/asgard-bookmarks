import datetime, urllib

from django.test import Client
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from tagging.models import Tag

from bookmarks.models import Bookmark

class BookmarkTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		self.user.is_staff = True
		self.user.save()
		
		self.bookmark = Bookmark()
		self.bookmark.title = 'Myles Braithwaite'
		self.bookmark.url = 'http://mylesbraithwaite.com/'
		self.bookmark.tags = 'myles braithwaite'
		self.bookmark.published = datetime.datetime.now()
		
		self.bookmark.author = self.user
		self.bookmark.save()
		
		self.site = Site(id=settings.SITE_ID, domain="example.com", name="example.com").save()
		
		self.client = Client()
	
	def tearDown(self):
		self.bookmark.delete()
		self.user.delete()
	
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
	
	def testBookmarkFeed(self):
		response = self.client.get(reverse('feeds', args=['bookmarks',]))
		self.assertEquals(response.status_code, 200)
	
	def testBookmarkTagFeed(self):
		response = self.client.get(reverse('feeds', args=['bookmarks-tag/myles']))
		self.assertEquals(response.status_code, 200)
	
	def testBookmarkSitemap(self):
		response = self.client.get(reverse('sitemap'))
		self.assertEquals(response.status_code, 200)
	
	def testURLtoAdminUnAuth(self):
		response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote(self.bookmark.url)))
		
		self.assertEquals(response.status_code, 302)
		self.assertTrue(response['Location'].endswith(
			self.bookmark.get_absolute_url()))
		
		response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote('http://www.google.com/')))
		self.assertEquals(response.status_code, 404)
	
	def testURLtoAdminAuth(self):
		self.client.login(username='john', password='johnpassword')
		response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote(self.bookmark.url)))
		
		self.assertEquals(response.status_code, 302)
		self.assertTrue(response['Location'].endswith(
			reverse('admin:bookmarks_bookmark_change', args=[self.bookmark.id,])))
		
		response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote('http://www.google.com/')))
		
		self.assertEquals(response.status_code, 302)