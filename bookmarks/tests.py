import datetime, urllib

from django.test import Client
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from bookmarks.models import Bookmark

class BookmarkTestCase(TestCase):
    
    fixtures = ['bookmarks.json',]
    
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_staff = True
        self.user.save()
        
        self.bookmark = Bookmark.objects.get(pk=1)
        
        self.bookmark.tags.add('Myles Braithwaite', 'Person')
        
        self.client = Client()
    
    def tearDown(self):
        self.bookmark.delete()
        self.user.delete()
    
    def testBookmarkIndex(self):
        response = self.client.get(reverse('bookmark_index'))
        self.assertEquals(response.status_code, 200)
    
    def testBookamrkPagnation(self):
        response = self.client.get(reverse('bookmark_index_paginated', args=[2,]))
        self.assertEquals(response.status_code, 200)
    
    def testBookmarkPagnationDoesNotExist(self):
        response = self.client.get(reverse('bookmark_index_paginated', args=[999,]))
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
        tag = self.bookmark.tags.all()[0]
        response = self.client.get(reverse('bookmark_tag_detail', args=[tag.slug,]))
        self.assertEquals(response.status_code, 200)
    
    def testTagPagnation(self):
        tag = self.bookmark.tags.all()[0]
        response = self.client.get(reverse('bookmark_tag_detail_paginated', args=[tag.slug, 2]))
        self.assertEquals(response.status_code, 200)
    
    def testTagPagnationDoesNotExist(self):
        tag = self.bookmark.tags.all()[0]
        response = self.client.get(reverse('bookmark_tag_detail_paginated', args=[tag.slug, 999]))
        self.assertEquals(response.status_code, 200)
    
    def testBookmarkSitemap(self):
        response = self.client.get(reverse('sitemap'))
        self.assertEquals(response.status_code, 200)
    
    def testURLtoAdminUnAuth(self):
        response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote(self.bookmark.url)))
        
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(
            self.bookmark.get_absolute_url()))
        
        response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote('http://www.example.org/')))
        self.assertEquals(response.status_code, 404)
    
    def testURLtoAdminAuth(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get("%s?url=%s" % (reverse('bookmark_url_redirect'), urllib.quote(self.bookmark.url)))
        
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(
            reverse('admin:bookmarks_bookmark_change', args=[self.bookmark.id,])))
        
        response = self.client.get("%(endpoint)s?url=%(url)s&title=%(title)s&body=%(body)s" % {
            'endpoint': reverse('bookmark_url_redirect'),
            'url': urllib.quote('http://www.google.com/'),
            'title': urllib.quote('Google'),
            'body': urllib.quote("A search engine.")
        })
        
        self.assertEquals(response.status_code, 302)