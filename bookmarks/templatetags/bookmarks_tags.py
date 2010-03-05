import re

from django import template
from django.conf import settings
from django.db import models

Bookmark = models.get_model('bookmarks', 'bookmark')

register = template.Library()

class LatestBookmarks(template.Node):
	"""
	Get a list of the latest bookmarks.
	"""
	def __init__(self, limit, var_name):
		self.limit = limit
		self.var_name = var_name
	
	def render(self, context):
		bookmarks = Bookmark.objects.published()[:int(self.limit)]
		
		if (int(self.limit) == 1):
			context[self.var_name] = bookmarks[0]
		else:
			context[self.var_name] = bookmarks
		
		return ''

@register.tag
def get_latest_bookmarks(parser, token):
	"""
	Gets any number of latest bookmarks and stores them in a varable.
	
	Syntax::
		
		{% get_latest_bookmarks [limit] as [var_name] %}
		
	Example usage::
		
		{% get_latest_bookmarks 10 as latest_bookmark_list %}
	"""
	try:
		tag_name, arg = token.contents.split(None, 1)
	except ValueError:
		raise template.TeamplteSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
	
	m = re.search(r'(.*?) as (\w+)', arg)
	
	if not m:
		raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
	
	format_string, var_name = m.groups()
	
	return LatestBookmarks(format_string[0], var_name)
