'''
Interesting notes on setting up Haystack + Elasticsearch:
https://gist.github.com/ramirezg/00d02ba2cbe85d522dfd
'''
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.utils.text import slugify

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

import library
import notebooks
import texts
from manuscripts.models import ManuscriptPage, Manuscript

from library.views import LibraryItemView, LibraryPageView
from notebooks.views import NotebookView, NotebookPageView
from texts.views import PageView

from connect.pathway import PathwayTree
from connect.graph import GraphLayout

from cache_utils.decorators import cached


import time

MODELVIEWS = {
    'libraryitem': LibraryItemView,
    'libraryexcerpt': LibraryPageView,
    'librarypage': LibraryPageView,
    'notebook': NotebookView,
    'note': NotebookPageView,
    'notebookpage': NotebookPageView,
    'line': PageView,
    'page': PageView,
}


class AdvancedSearchView(SearchView):
    '''Overrides the Haystack view'''
    template = 'search/advanced_search.html'
    form = HighlightedModelSearchForm()


class StatsView(TemplateView):

    template_name = 'JJDLP/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        context['library_items'] = library.models.LibraryItem.objects.count()
        context['library_traces'] = library.models.LibraryExcerpt.objects.count()
        context['notebooks'] = notebooks.models.Notebook.objects.count()
        context['notebooks_notes'] = notebooks.models.Note.objects.count()
        context['manuscript_collections'] = Manuscript.objects.count()
        context['manuscript_pages'] = ManuscriptPage.objects.count()
        context['novels'] = texts.models.Text.objects.count()
        context['novels_pages'] = texts.models.Page.objects.count()

        return context


class DocsView(TemplateView):
    template_name = 'JJDLP/docs.html'
    raw = False

    def docs(self):
        return open('DOCS.txt', 'r').read()


class ConnectView(TemplateView):
    template_name = 'JJDLP/connect.html'


# @cached(60*5)
def make_tree(root, model, upstream=True, downstream=True):
    start_time = time.time()
    tree = PathwayTree(root, model)
    # tree.set_query(upstream, downstream)
    tree.grow(4)
    print("--- %s seconds ---" % (time.time() - start_time))
    return tree


class ConnectTree(View):
    '''
    View to receive JSON data for Tree objects.

    request: root and model
    response: PathwayTree object as JSON
    '''
    req = ''

    def get(self, request, *args, **kwargs):
        # if request.is_ajax():
        root, model, up, down = self.get_tree_input(request)
        # first create tree; this must be cached!
        tree = make_tree(slugify(root), str(model), upstream=up, downstream=down)

        if self.req == 'tree':
            # create a graph layout for the tree
            graph = GraphLayout(tree)
            return JsonResponse(graph.layout)

        elif self.req == 'path':
            # find requested path
            nodeName = request.GET.get('nodename')
            nodeName = nodeName.encode('utf-8')
            tree.select_branch(nodeName)
            # create a graph layout for the tree
            graph = GraphLayout(tree)
            return JsonResponse(graph.branchlayout())

    def get_tree_input(self, request):
        root = request.GET.get('rootid')
        model = request.GET.get('modelid')
        up = request.GET.get('upstream')
        down = request.GET.get('downstream')
        return root, model, up, down
