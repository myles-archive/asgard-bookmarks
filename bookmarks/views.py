import re
import urllib

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers

from tagging.models import TaggedItem, Tag

from bookmarks.forms import STOP_WORDS, BookmarksSearchForm
from bookmarks.models import Bookmark

def index(request, page=1, context={}, template_name='bookmarks/index.html'):
	"""
	The bookmarks index page.
	"""
	bookmark_list = Bookmark.objects.all()
	paginator = Paginator(bookmark_list, 20)
	
	try:
		bookmarks = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)
	
	context.update({
		'bookmarks':	bookmarks,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def detail(request, uuid, context={}, template_name='bookmarks/detail.html'):
	"""
	The bookmark detail page.
	"""
	try:
		bookmark = Bookmark.objects.select_related().get(uuid=uuid)
	except Bookmark.DoesNotExist:
		raise Http404
	
	related = TaggedItem.objects.get_related(bookmark, Bookmark, num=5)
	
	tags = Tag.objects.get_for_object(bookmark).select_related()
	context.update({ 'bookmark': bookmark, 'tags': tags, 'related': related })
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_list(request, context={}, template_name='bookmarks/tag_list.html'):
	context.update({
		'is_archive': True,
	})
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_detail(request, tag, page=1, context={}, template_name='bookmarks/tag_detail.html'):
	try:
		tag_object = Tag.objects.get(name=urllib.unquote(tag))
	except Tag.DoesNotExist:
		raise Http404
	
	bookmark_list = TaggedItem.objects.get_by_model(Bookmark, tag_object) 
	paginator = Paginator(bookmark_list, 20)
	
	try:
		bookmarks = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)
	
	context.update({
		'tag': tag_object,
		'bookmarks': bookmarks,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def search(request, context={}, template_name='bookmarks/search.html'):
	if request.GET:
		new_data = request.GET.copy()
		form = BookmarksSearchForm(new_data)
		if form.is_valid():
			stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
			search_term = form.cleaned_data['q']
			cleaned_search_term = stop_word_list.sub('', search_term)
			if cleaned_search_term:
				query = Bookmark.objects.search(cleaned_search_term.strip())
			else:
				query = None

			context.update({
				'results': query,
				'query': form.cleaned_data['q'],
				'form': form,
				'is_archive': True,
			})
		else:
			pass
	else:
		form = BookmarksSearchForm()
		context.update({
			'form': form,
			'is_archive': True,
		})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def url_redirect(request):
	url = request.GET.get('url')
	
	try:
		bookmark = Bookmark.objects.get(url__startswith=urllib.unquote(url))
	except Bookmark.DoesNotExist:
		bookmark = None
	
	if bookmark:
		if request.user.is_staff:
			return HttpResponseRedirect(
				urlresolvers.reverse('admin:bookmarks_bookmark_change', args=[bookmark.id,]))
		else:
			return HttpResponseRedirect(bookmark.get_absolute_url())
	else:
		if request.user.is_staff:
			return HttpResponseRedirect(
				urlresolvers.reverse('admin:bookmarks_bookmark_add') +
				"?" + urllib.urlencode(request.GET))
		else:
			raise Http404