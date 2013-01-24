from django.conf.urls import *
from django.contrib import admin

from bookmarks.sitemaps import BookmarkSitemap, BookmarkTagSitemap
from bookmarks.feeds import BookmarkFeed, BookmarkTagFeed

admin.autodiscover()

sitemaps = {
	'bookmarks': BookmarkSitemap,
	'bookmarks-tags': BookmarkTagSitemap,
}

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	(r'^bookmarks/', include('bookmarks.urls')),
	
	url(r'^sitemap.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{ 'sitemaps': sitemaps },
		name = 'sitemap'
	),
)