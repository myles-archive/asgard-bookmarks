from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from tagging.models import TaggedItem, Tag

from asgard.bookmarks.models import Bookmark

class BookmarkSitemap(Sitemap):
	changefreq = "never"
	priority = 1.0
	
	def items(self):
		return Bookmark.objects.published()
	
	def lastmod(self, obj):
		return obj.published
	
	def location(self, obj):
		return obj.get_absolute_url()

class BookmarkTagSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.1
	
	def items(self):
		return Tag.objects.usage_for_model(Bookmark)
	
	def lastmod(self, obj):
		try:
			bookmark = TaggedItem.objects.get_by_model(Bookmark, obj)[0]
		except IndexError:
			return None
		return bookmark.published
	
	def location(self, obj):
		return reverse('bookmark_tag_detail', args=[obj.name,])
