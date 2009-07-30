from django.conf.urls.defaults import *

urlpatterns = patterns('asgard.bookmarks.views',
	url(r'^tag/(?P<tag>(.*))/(?P<page>\d+)/$',
		view = 'tag_detail',
		name = 'bookmark_tag_detail_paginated',
	),
	url(r'^tag/(?P<tag>(.*))/$',
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
