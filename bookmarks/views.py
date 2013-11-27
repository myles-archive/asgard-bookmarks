import re
import urllib

from django.core import urlresolvers
from django.contrib.auth.models import User

from django.http import (
    Http404,
    HttpResponseRedirect,
)

from django.core.paginator import (
    EmptyPage,
    Paginator,
    InvalidPage,
)

from django.views.generic.base import (
	View,
	ContextMixin,
	TemplateResponseMixin
)

from taggit.models import Tag

from bookmarks.models import Bookmark
from bookmarks.settings import BOOKMARKS_PAGINATE_BY
from bookmarks.forms import STOP_WORDS, BookmarksSearchForm

class BookmarkListView(TemplateResponseMixin, ContextMixin, View):
    """
    The bookmarks index page.
    """
    
    template_name = 'bookmarks/index.html'
    
    def get(self, request, page=1, count=BOOKMARKS_PAGINATE_BY, *args, **kwargs):
        bookmark_list = Bookmark.objects.published()
        
        if not bookmark_list:
            raise Http404
        
        paginator = Paginator(bookmark_list, int(request.GET.get('count', count)))
        
        try:
            bookmarks = paginator.page(int(request.GET.get('page', page)))
        except (EmptyPage, InvalidPage):
            bookmarks = paginator.page(paginator.num_pages)
        
        context = self.get_context_data(bookmarks=bookmarks)
        
        return self.render_to_response(context)

class BookmarkDetailView(TemplateResponseMixin, ContextMixin, View):
    """
    The bookmark detail page.
    """
    
    template_name = 'bookmarks/detail.html'
    
    def get(self, request, uuid, *args, **kwargs):
        try:
            bookmark = Bookmark.objects.select_related().get(uuid=uuid)
        except Bookmark.DoesNotExist:
            raise Http404
        
        # related = TaggedItem.objects.get_related(bookmark, Bookmark, num=5)
        related = None
        
        context = self.get_context_data(bookmark=bookmark, related=related)
        
        return self.render_to_response(context)

class BookmarkTagListView(TemplateResponseMixin, ContextMixin, View):
    
    template_name = 'bookmarks/tag_list.html'
    
    def get(self, request, *args, **kwargs):
        tags = Bookmark.tags.all()
        
        context = self.get_context_data(tags=tags, is_archive=True)
        
        return self.render_to_response(context)

class BookmarkTagDetailView(TemplateResponseMixin, ContextMixin, View):
    
    template_name = 'bookmarks/tag_detail.html'
    
    def get(self, request, slug, page=1, count=BOOKMARKS_PAGINATE_BY, *args, **kwargs):
    	try:
    		tag = Bookmark.tags.get(slug=urllib.unquote(slug))
    	except Tag.DoesNotExist:
    		raise Http404
	
    	bookmark_list = Bookmark.objects.filter(tags__in=[tag])
	
    	paginator = Paginator(bookmark_list, int(request.GET.get('count', count)))
	
    	try:
    		bookmarks = paginator.page(int(request.GET.get('page', page)))
    	except (EmptyPage, InvalidPage):
    		bookmarks = paginator.page(paginator.num_pages)
        
        context = self.get_context_data(tag=tag, bookmarks=bookmarks, is_archive=True)
        
        return self.render_to_response(context)

class BookmarkAuthorListView(TemplateResponseMixin, ContextMixin, View):
    
    template_name = 'bookmarks/author_list.html'
    
    def get(self, request, *args, **kwargs):
        authors = User.objects.filter(is_staff=True)
        
        context = self.get_context_data(authors=authors, is_archive=True)
        
        return self.render_to_response(context)

class BookmarkAuthorDetailView(TemplateResponseMixin, ContextMixin, View):
    
    template_name = 'bookmarks/author_detail.html'
    
    def get(self, request, username, page=1, count=BOOKMARKS_PAGINATE_BY, *args, **kwargs):
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
        
        context = self.get_context_data(author=author, bookmarks=bookmarks, is_archive=True)
        
        return self.render_to_response(context)

class BookmarkSearchView(TemplateResponseMixin, ContextMixin, View):
    
    template_name = 'bookmarks/search.html'
    
    def get(self, request, *args, **kwargs):
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
                
                context = self.get_context_data(
                    results=query,
                    query=form.cleaned_data['q'],
                    form=form,
                    is_archive=True
                )
            else:
                raise Http404
    	else:
    		form = BookmarksSearchForm()
    		context = self.get_context_data(
                form=form,
                is_archive=True
            )
    	
    	return self.render_to_response(context)

class BookmarkURLRedirectView(View):
    
    def get(self, request, *args, **kwargs):
    	url = request.GET.get('url')
    	title = request.GET.get('title', None)
    	body = request.GET.get('body', None)
        
        try:
            bookmark = Bookmark.objects.get(url__startswith=urllib.unquote(url))
        except Bookmark.DoesNotExist:
            bookmark = None
        
        if bookmark and request.user.is_staff:
    		return HttpResponseRedirect(
    			urlresolvers.reverse(
    				'admin:bookmarks_bookmark_change',
    				args=[bookmark.id,]
    			)
    		)
        
        if bookmark:
            return HttpResponseRedirect(bookmark.get_absolute_url())
        
        if not bookmark and request.user.is_staff:
			return HttpResponseRedirect("%(endpoint)s?_popup=1&url=%(url)s&title=%(title)s&body=%(body)s" % {
				'endpoint': urlresolvers.reverse('admin:bookmarks_bookmark_add'),
				'url': url,
				'title': title,
				'body': body,
			})
        
        raise Http404