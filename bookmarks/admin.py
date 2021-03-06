from django.contrib import admin

from bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('title', 'url', 'published', '_get_tags')
	list_filter = ('published',)
	exclude = ['uuid',]
	date_hierarchy = 'published'

admin.site.register(Bookmark, BookmarkAdmin)