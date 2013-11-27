from django.contrib import admin
from django.conf.urls import patterns, url, include

from bookmarks.sitemaps import BookmarkSitemap, BookmarkTagSitemap

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