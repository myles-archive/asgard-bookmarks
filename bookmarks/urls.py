from django.conf.urls.defaults import *

from bookmarks.feeds import BookmarkFeed, BookmarkTagFeed

urlpatterns = patterns('',
	url(r'feed/$',
		view = BookmarkFeed(),
		name = 'bookmarks_bookmark_feed',
	),
	url(r'tag/(?P<slug>(.*))/feed/$',
		view = BookmarkTagFeed,
		name = 'bookmarks_bookmark_tag_feed'
	)
)

urlpatterns += patterns('bookmarks.views',
	url(r'^url/$',
		view = 'url_redirect',
		name = 'bookmark_url_redirect',
	),
	url(r'^tag/(?P<tag>(.*))/(?P<page>\d+)/$',
		view = 'tag_detail',
		name = 'bookmark_tag_detail_paginated',
	),
	url(r'^tag/(?P<slug>(.*))/$',
		view = 'tag_detail',
		name = 'bookmark_tag_detail',
	),
	url(r'^tag/$',
		view = 'tag_list',
		name = 'bookmark_tag_list'
	),
	url(r'^search/$',
		view = 'search',
		name = 'bookmark_search'
	),
	url(r'^page/(?P<page>\d+)/$',
		view = 'index',
		name = 'bookmark_index_paginated',
	),
	url(r'(?P<uuid>[-\w]+)/$',
		view = 'detail',
		name = 'bookmark_detail'
	),
	url(r'^$',
		view = 'index',
		name = 'bookmark_index',
	),
)