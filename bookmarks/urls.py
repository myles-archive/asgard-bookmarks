from django.conf.urls import patterns, url

from bookmarks.views import (
    BookmarkListView,
    BookmarkDetailView,
    
    BookmarkTagListView,
    BookmarkTagDetailView,
    
    BookmarkAuthorListView,
    BookmarkAuthorDetailView,
    
    BookmarkSearchView,
    
    BookmarkURLRedirectView,
)

from bookmarks.feeds import (
    BookmarkFeed,
    BookmarkTagFeed,
    BlogAuthorPostFeed
)

urlpatterns = patterns('',
	url(r'^feed/$',
		view = BookmarkFeed(),
		name = 'bookmarks_bookmark_feed',
	),
	url(r'^tag/(?P<slug>(.*))/feed/$',
		view = BookmarkTagFeed(),
		name = 'bookmarks_bookmark_tag_feed'
	),
	url(r'^author/(?P<username>[-\w]+)/feed/$',
		view = BlogAuthorPostFeed(),
		name = 'bookmarks_bookmark_author_feed'
	)
)

urlpatterns += patterns('bookmarks.views',
	url(r'^url/$',
		view = BookmarkURLRedirectView.as_view(),
		name = 'bookmark_url_redirect',
	),
	url(r'^tag/(?P<slug>(.*))/(?P<page>\d+)/$',
		view =  BookmarkTagDetailView.as_view(),
		name = 'bookmark_tag_detail_paginated',
	),
	url(r'^tag/(?P<slug>(.*))/$',
		view = BookmarkTagDetailView.as_view(),
		name = 'bookmark_tag_detail',
	),
	url(r'^tag/$',
		view = BookmarkTagListView.as_view(),
		name = 'bookmark_tag_list'
	),
	url(r'^author/(?P<username>(.*))/(?P<page>\d+)/$',
		view = BookmarkAuthorDetailView.as_view(),
		name = 'bookmarks_authors_detail_paginated',
	),
	url(r'^author/(?P<username>(.*))/$',
		view = BookmarkAuthorDetailView.as_view(),
		name = 'bookmarks_authors_detail',
	),
	url(r'^author/$',
		view = BookmarkAuthorListView.as_view(),
		name = 'bookmarks_author_list'
	),
	url(r'^search/$',
		view = BookmarkSearchView.as_view(),
		name = 'bookmark_search'
	),
	url(r'^page/(?P<page>\d+)/$',
		view = BookmarkListView.as_view(),
		name = 'bookmark_index_paginated',
	),
	url(r'(?P<uuid>[-\w]+)/$',
		view = BookmarkDetailView.as_view(),
		name = 'bookmark_detail'
	),
	url(r'^$',
		view = BookmarkListView.as_view(),
		name = 'bookmark_index',
	),
)
