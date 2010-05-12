from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

from tagging.models import TaggedItem, Tag

from bookmarks.models import Bookmark

class BookmarkFeed(Feed):
	_site = Site.objects.get_current()
	title = u"%s: bookmarks." % _site.name
	subtitle = u"More than a hapax legomenon."
	title_template = 'feeds/bookmarks_bookmark_title.html'
	description_template = 'feeds/bookmarks_bookmark_description.html'
	
	def link(self):
		return "%s" % reverse('bookmark_index')
	
	def items(self):
		return Bookmark.objects.published()[:10]
	
	def item_link(self, item):
		return "%s%s" % (item.get_absolute_url(), "?utm_source=feedreader&utm_medium=feed&utm_campaign=BookmarkFeed")
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return "%s" % item.get_absolute_url()
	
	def item_categories(self, item):
		return item.tags.all()

class BookmarkTagFeed(Feed):
	subtitle = u"More than a hapax legomenon."
	title_template = 'feeds/bookmarks_bookmark_title.html'
	description_template = 'feeds/bookmarks_bookmark_description.html'
	
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return Bookmark.tags.get(slug=bits[0])
	
	def title(self, obj):
		_site = Site.objects.get_current()
		return "%s: bookmarks tagged in %s." % (_site.name, obj.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return reverse('bookmark_tag_detail', args=[obj.slug,])
	
	def items(self, obj):
		return Bookmark.objects.filter(tags__in=[obj])
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogTagPostFeed"
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return "%s" % item.get_absolute_url()
	
	def item_categories(self, item):
		return item.tags.all()