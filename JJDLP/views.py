'''
Interesting notes on setting up Haystack + Elasticsearch:
https://gist.github.com/ramirezg/00d02ba2cbe85d522dfd
'''
from django.views.generic import View, TemplateView
from django.http import JsonResponse

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from notebooks.models import Notebook, Note
from library.models import LibraryItem, LibraryExcerpt, Author, Publisher
from manuscripts.models import ManuscriptCollection, ManuscriptPage
from novels.models import Novel, Page
from generic.views.json import JsonView

from connect.pathway import PathwayTree
from connect.graph import GraphLayout

from cache_utils.decorators import cached

LIBRARY_AUTHOR = 'libraryauthor'
LIBRARY_PUBLISHER = 'librarypublisher'
LIBRARY_ITEM = 'libraryitem'
LIBRARY_EXCERPT = 'libraryexcerpt'
NOTEBOOKS_NOTEBOOK = 'notebook'
NOTEBOOKS_NOTE = 'note'


class AdvancedSearchView(SearchView):
    '''Overrides the Haystack view'''
    template = 'search/advanced_search.html'
    form = HighlightedModelSearchForm()


class StatsView(TemplateView):

    template_name = 'JJDLP/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        context['library_items'] = LibraryItem.objects.count()
        context['library_traces'] = LibraryExcerpt.objects.count()
        context['notebooks'] = Notebook.objects.count()
        context['notebooks_notes'] = Note.objects.count()
        context['manuscript_collections'] = ManuscriptCollection.objects.count()
        context['manuscript_pages'] = ManuscriptPage.objects.count()
        context['novels'] = Novel.objects.count()
        context['novels_pages'] = Page.objects.count()

        return context


class DocsView(TemplateView):
    template_name = 'JJDLP/docs.html'
    raw = False

    def docs(self):
        return open('DOCS.txt', 'r').read()


class ConnectView(TemplateView):
    template_name = 'JJDLP/connect.html'


class ConnectDatabase(JsonView):
    '''
    View for quickly getting database information.
    Can be seen as a kind of REST module.

    request: model and (optional) primary key (pk)
    response: database access in JSON
    '''
    def process_request(self, request):
        # override
        model = request.GET.get('model')
        pk = request.GET.get('pk')
        return (model, pk)

    def request_database(self, processed_data):
        '''
        Get items from the database according to the requested input.
        With this function, it is possible to filter which part of
        the data can be made available to the user.

        input: String model, according to constants
                String pk, primary key of item of interest
        output: QuerySet with items that match the request, or empty list
                if none matched.
        '''
        # override
        model, pk = processed_data
        items = []
        if pk:
            if model == LIBRARY_ITEM:
                items = LibraryItem.objects.filter(pk=pk)
            elif model == LIBRARY_EXCERPT:
                items = LibraryExcerpt.objects.filter(pk=pk)
            elif model == NOTEBOOKS_NOTEBOOK:
                items = Notebook.objects.filter(pk=pk)
            elif model == NOTEBOOKS_NOTE:
                items = Note.objects.filter(pk=pk)
        else:
            if model == LIBRARY_ITEM:
                items = LibraryItem.objects.all()
            elif model == LIBRARY_AUTHOR:
                items = Author.objects.all()
            elif model == LIBRARY_PUBLISHER:
                items == Publisher.objects.all()
            elif model == LIBRARY_EXCERPT:
                items = LibraryExcerpt.objects.all()
            elif model == NOTEBOOKS_NOTEBOOK:
                items = Notebook.objects.all()
            elif model == NOTEBOOKS_NOTE:
                items = Note.objects.all()
        return items

    def get_claims(self):
        # override
        claim = {}
        claim['developer'] = 'Tom De Keyser'
        claim['developed_at'] = 'Centre for Manuscript Genetics'
        claim['supervised_by'] = ['Dirk Van Hulle', 'Geert Lernout']
        claim['developer_link'] = 'https://www.uantwerpen.be/en/rg/centre-for-manuscript-genetics/'
        return claim


@cached(60*5)
def make_tree(root, model):
    tree = PathwayTree(str(root), str(model))
    tree.grow(3)
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
        root, model = self.get_tree_input(request)
        # first create tree; this must be cached!
        tree = make_tree(str(root), str(model))

        if self.req == 'tree':
            # create a graph layout for the tree
            graph = GraphLayout(tree)
            return JsonResponse(graph.layout)

        elif self.req == 'path':
            # find requested path
            nodeName = request.GET.get('nodename')
            tree.select_branch(nodeName)
            # create a graph layout for the tree
            graph = GraphLayout(tree)
            return JsonResponse(graph.branchlayout())

    def get_tree_input(self, request):
        root = request.GET.get('rootid')
        model = request.GET.get('modelid')
        return root, model
