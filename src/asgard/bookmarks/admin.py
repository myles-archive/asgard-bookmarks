from django.contrib import admin

from asgard.bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('title', 'url', 'publiched',)
	list_filter = ('published',)
	exclude = ['uuid',]
	date_hierarchy = 'published'

admin.site.register(Bookmark, BookmarkAdmin)
