import re
import urllib

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core import urlresolvers

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
	
	# related = TaggedItem.objects.get_related(bookmark, Bookmark, num=5)
	related = None
	
	context.update({ 'bookmark': bookmark, 'related': related })
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_list(request, context={}, template_name='bookmarks/tag_list.html'):
	tags = Bookmark.tags.all()
	
	context.update({
		'tags': tags,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_detail(request, slug, page=1, context={}, template_name='bookmarks/tag_detail.html'):
	
	tag = Bookmark.tags.get(slug=urllib.unquote(slug))
	bookmark_list = Bookmark.objects.filter(tags__in=[tag])
	
	paginator = Paginator(bookmark_list, 20)
	
	try:
		bookmarks = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)
	
	context.update({
		'tag': tag,
		'bookmarks': bookmarks,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def author_list(request, context={}, template_name='bookmarks/author_list.html'):
	authors = User.objects.filter(is_staff=True)

	context.update({
		'authors': authors,
		'is_archive': True
	})

	return render_to_response(template_name, context, context_instance=RequestContext(request))

def author_detail(request, username, page=1, count=5, context={}, template_name="bookmarks/author_detail.html"):
	try:
		author = User.objects.get(username__iexact=username)
	except User.DoesNotExist:
		raise Http404

	bookmark_list = Bookmark.objects.published(author=author)

	paginator = Paginator(bookmark_list, int(request.GET.get('count', count)))

	try:
		bookmarks = paginator.page(int(request.GET.get('page', page)))
	except (EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)

	context.update({
		'author': author,
		'bookmarks': bookmarks,
		'is_archive': True
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
				"%s?url=%s" % (urlresolvers.reverse('admin:bookmarks_bookmark_add'),
					url))
		else:
			raise Http404