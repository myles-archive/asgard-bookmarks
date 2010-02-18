from urllib import quote_plus

try:
    from uuid import NAMESPACE_URL, uuid3
except ImportError:
    from bookmarks.uuid import NAMESPACE_URL, uuid3

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from tagging import register as tags_register
from tagging.fields import TagField

from asgard.utils.db.fields import MarkupTextField

from bookmarks.managers import BookmarkManager

class Bookmark(models.Model):
	uuid = models.CharField(_('UUID'), max_length=36, unique=True)
	title = models.CharField(_('title'), max_length=1000)
	body = MarkupTextField(_('body'), null=True, blank=True)
	url = models.URLField(_('URL'), max_length=1000)
	tags = TagField(_('Tags'), max_length=1000)
	
	author = models.ForeignKey(User, verbose_name=_('author'))
	
	published = models.DateTimeField(_('published'))
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	objects = BookmarkManager()
	
	class Meta:
		verbose_name = _('bookmark')
		verbose_name_plural = _('bookmarks')
		db_table = 'bookmarks'
		ordering = ('-published',)
	
	@property
	def url_safe(self):
		return quote_plus(self.url)
	
	def save(self, **kwargs):
		uuid = uuid3(NAMESPACE_URL, str(self.url))
		self.uuid = str(uuid)
		super(Bookmark, self).save(kwargs)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('bookmark_detail', None, {
			'uuid':	self.uuid,
		})
	
	def get_internal_url(self):
		"""
		For backwards compatibility.
		"""
		return self.get_absolute_url()

tags_register(Bookmark, 'tag_set')
