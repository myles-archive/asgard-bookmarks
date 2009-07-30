import urllib

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tagging.models import TaggedItem, Tag
from asgard.bookmarks.models import Bookmark
from asgard.utils.search import STOP_WORDS, SearchForm

def index(request, page=1, context={}, template_name='bookmarks/index.html'):
	"""
	The bookmarks index page.
	"""
	link_list = Bookmark.objects.all()
	paginator = Paginator(link_list, 20)
	
	try:
		links = paginator.page(page)
	except (EmptyPage, InvalidPage):
		links = paginator.page(paginator.num_pages)
	
	context.update({
		'links':				links.object_list,
		'has_next':				links.has_next(),
		'has_other_pages':		links.has_other_pages(),
		'has_previous':			links.has_previous(),
		'next_page_number':		links.next_page_number(),
		'previous_page_number':	links.previous_page_number(),
		'start_index':			links.start_index(),
		'end_index':			links.end_index(),
		'page_number':			links.number,
		'page_range':           links.paginator.page_range
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def detail(request, uuid, context={}, template_name='bookmarks/detail.html'):
	"""
	The bookmark detail page.
	"""
	try:
		link = Bookmark.objects.select_related().get(uuid=uuid)
	except Bookmark.DoesNotExist:
		raise Http404
	
	related = TaggedItem.objects.get_related(link, Bookmark, num=5)
	
	tags = Tag.objects.get_for_object(link).select_related()
	context.update({ 'link': link, 'tags': tags, 'related': related })
	
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
	
	link_list = TaggedItem.objects.get_by_model(Bookmark, tag_object) 
	paginator = Paginator(link_list, 20)
	
	try:
		links = paginator.page(page)
	except (EmptyPage, InvalidPage):
		links = paginator.page(paginator.num_pages)
	
	context.update({
		'tag': tag_object,
		'links': links.object_list,
		'has_next': links.has_next(),
		'has_previous': links.has_previous(),
		'has_other_pages': links.has_other_pages(),
		'start_index': links.start_index(),
		'end_index': links.end_index(),
		'previous_page_number': links.previous_page_number(),
		'next_page_number': links.next_page_number(),
		'page_number': links.number,
		'page_range': links.paginator.page_range,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

try:
	import djapian
except ImportError:
	djapian = None

def search(request, context={}, template_name='bookmarks/search.html'):
	if request.GET:
		new_data = request.GET.copy()
		form = SearchForm(new_data)
		if form.is_valid():
			if djapian:
				from asgard.bookmarks.index import Bookmark as BookmarkIndex
				search = BookmarkIndex.indexer.search(form.cleaned_data['q'])
				query = [s.instance for s in search]
			else:
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
		form = SearchForm()
		context.update({
			'form': form,
			'is_archive': True,
		})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))
