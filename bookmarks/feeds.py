from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed, FeedDoesNotExist

from bookmarks.models import Bookmark

current_site = Site.objects.get_current()

class BaseFeed(Feed):
	subtitle = u"More than a hapax legomenon."
	title_description = 'feeds/bookamrks_boomark_title.html'
	description_template = 'feeds/bookamrks_boomark_description.html'
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return item.get_absolute_url()
	
	def item_author_name(self, item):
		return u"%s %s" % (item.author.first_name, item.author.last_name)
	
	def item_author_email(self, item):
		return u"%s" % (item.author.email)
	
	def item_author_link(self, item):
		return reverse('bookmarks_authors_detail', args=[item.author.username,])
	
	def item_categories(self, item):
		return item.tags.all()
	
	def item_copyright(self, item):
		return u"Copyright (c) %s, %s %s" % (current_site.name, item.author.first_name, item.author.last_name)
	
	def feed_title(self):
		return u"%s" % current_site.name
	
	def feed_authors(self):
		return ({"name": user.name} for user in User.objects.filter(is_staff=True))

class BookmarkFeed(BaseFeed):
	title = u"%s: bookmarks." % current_site.name
	
	def link(self):
		return reverse('bookmark_index')
	
	def items(self):
		return Bookmark.objects.published()[:10]

class BookmarkTagFeed(BaseFeed):
	def get_object(self, request, slug):
		return Bookmark.tags.get(slug=slug)
	
	def title(self, obj):
		_site = Site.objects.get_current()
		return "%s: bookmarks tagged in %s." % (_site.name, obj.name)
	
	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return reverse('bookmark_tag_detail', args=[obj.slug,])
	
	def items(self, obj):
		return Bookmark.objects.filter(tags__in=[obj])

class BlogAuthorPostFeed(BaseFeed):
	def get_object(self, request, username):
		return User.objects.filter(username_exact=username, is_staff=True)
	
	def title(self, obj):
		if obj.get_full_name():
			name = obj.get_full_name()
		else:
			name = obj.username
		return u"%s: weblog entries written by %s." % (current_site.name, name)
	
	def link(self, obj):
		return reverse('bookmarks_authors_detail', args=[obj.username,])
	
	def items(self, obj):
		return Post.objects.published(author=obj)
