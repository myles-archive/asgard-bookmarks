from django.conf import settings

BOOKMARKS_PAGINATE_BY = getattr(settings, 'BOOKMARKS_PAGINATE_BY', 20)
BOOKMARKS_MULTIPLE_SITES = getattr(settings, 'BOOKMARKS_MULTIPLE_SITES', False)