from haystack import site, indexes

from asgard.bookmarks.models import Bookmark

class BookmarkIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	published = indexes.DateTimeField(model_attr='published')
	
	def get_query_set(self):
		return Bookmark.objects.published()

site.register(Bookmark, BookmarkIndex)