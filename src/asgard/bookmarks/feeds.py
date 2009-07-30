from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from asgard.bookmarks.models import Bookmark

class BookmarkFeed(Feed):
	_site = Site.objects.get_current()
	title = u"%s: latest bookmarks." % _site.name
	subtitle = u"More than a hapax legomenon."
	title_template = 'feeds/bookmarks_bookmark_title.html'
	description_tempalte = 'feeds/bookmarks_bookmark_description.html'
	
	def index(self):
		return u"%s" % reverse('bookmarks_index')
	
	def items(self):
		return Bookmark.objects.published()[:10]
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BookmarkFeed"
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return u"%s" % item.get_absolute_url()
