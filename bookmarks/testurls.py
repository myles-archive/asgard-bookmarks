from django.conf.urls.defaults import *
from django.contrib import admin

from bookmarks.sitemaps import BookmarkSitemap, BookmarkTagSitemap
from bookmarks.feeds import BookmarkFeed, BookmarkTagFeed

admin.autodiscover()

feeds = {
	'bookmarks': BookmarkFeed,
	'bookmarks-tag': BookmarkTagFeed,
}

sitemaps = {
	'bookmarks': BookmarkSitemap,
	'bookmarks-tags': BookmarkTagSitemap,
}

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	(r'^bookmarks/', include('bookmarks.urls')),
	
	url(r'^feeds/(?P<url>.*)/$',
		'django.contrib.syndication.views.feed',
		{ 'feed_dict': feeds },
		name = 'feeds'
	),
	
	url(r'^sitemap.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{ 'sitemaps': sitemaps },
		name = 'sitemap'
	),
)