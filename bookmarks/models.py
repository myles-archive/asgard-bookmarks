from urllib import quote_plus

try:
    from uuid import NAMESPACE_URL, uuid3
except ImportError:
    from bookmarks.uuid import NAMESPACE_URL, uuid3

from django.db import models
from django.utils.text import slugify
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from taggit.managers import TaggableManager

try:
	from django_markup.fields import MarkupField
except ImportError:
	MarkupField = False

from bookmarks.managers import BookmarkManager

class Bookmark(models.Model):
	uuid = models.CharField(_('UUID'), max_length=36, unique=True)
	title = models.CharField(_('title'), max_length=1000)
	body = models.TextField(_('body'), null=True, blank=True)
	url = models.URLField(_('URL'), max_length=1000)
	
	author = models.ForeignKey(User, verbose_name=_('author'))
	
	published = models.DateTimeField(_('published'))
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	comments = generic.GenericRelation(Comment, object_id_field='object_pk')
	
	tags = TaggableManager()
	
	if MarkupField:
		markup = MarkupField(default='none')
	
	sites = models.ManyToManyField(Site, blank=True, null=True)
	
	objects = BookmarkManager()
	
	class Meta:
		verbose_name = _('bookmark')
		verbose_name_plural = _('bookmarks')
		db_table = 'bookmarks'
		ordering = ('-published',)
	
	@property
	def slug(self):
		return slugify(self.title)
	
	@property
	def url_safe(self):
		return quote_plus(self.url)
	
	def save(self, **kwargs):
		uuid = uuid3(NAMESPACE_URL, str(self.url))
		self.uuid = str(uuid)
		
		super(Bookmark, self).save(**kwargs)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('bookmark_detail', None, {
			'uuid':	self.uuid,
			'slug': self.slug,
		})
	
	def get_internal_url(self):
		"""
		For backwards compatibility.
		"""
		return self.get_absolute_url()
	
	def _get_tags(self):
		tag_string = ''
		for t in self.tags.all():
			link = '<a href="./?tags__id__exact=%s" title="Show all post under %s tag">%s</a>' % (t.slug, t.name, t.name)
			link = u"%s" % t.name
			tag_string = ''.join([tag_string, link, ', '])
		return tag_string.rstrip(', ')
	
	_get_tags.short_description = _('Tags')
	_get_tags.allow_tags = True