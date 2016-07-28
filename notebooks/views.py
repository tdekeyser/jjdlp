from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from notebooks.models import Notebook, NotebookPage, Note
from gentext.views.item import ItemView
from gentext.views.page import PageView

notebooks_dummy_base = 'notebooks/dummy_base.html'


class NotebookHomeView(TemplateView):
    '''
    NOTEBOOKS_HOME presents:
        - short information on notebooks section
        - search functionality
        - a list of all available notebooks
        - amount of notebooks and notes
    '''
    template_name = 'notebooks/base.html'

    def get_context_data(self, **kwargs):
        context = super(NotebookHomeView, self).get_context_data(**kwargs)
        context['notebooks'] = Notebook.objects.all()
        context['counted_notebooks'] = Notebook.objects.all().count()
        context['counted_notes'] = Note.objects.all().count()

        # notebook images
        context['b1frontcover'] = NotebookPage.objects.filter(page_number__contains='frontcover').order_by('?').first()
        context['c_example'] = None
        context['d_example'] = None

        return context


class NoteSearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'notebooks/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=notebooks.note'}


class NotebookView(ItemView):
    paginate_by = 8
    model = Notebook

    template = 'notebooks/item.html'
    dummybase_template = notebooks_dummy_base

    def get_item(self):
        # override
        return self.model.objects.get(name=self.kwargs['noteb'])

    def all_pages(self):
        return self.pages().all()

    def all_lib_items(self):
        return self.item.libraryitem.all()


class NotebookPageView(PageView):
    parent_model = Notebook
    itemslug = 'noteb'
    pageslug = 'notebpage'

    template = 'notebooks/page.html'
    dummybase_template = notebooks_dummy_base

    def get_item(self):
        # override
        return self.parent_model.objects.get(name=self.kwargs[self.itemslug])

    def get_page(self):
        # override
        return self.pageQ.get(page_number=self.kwargs[self.pageslug])

    def get_context_data(self, **kwargs):
        # override
        context = super(NotebookPageView, self).get_context_data(**kwargs)
        notes = self.object.note_set.all()
        if notes:
            context['notes'] = notes
        #     traced_objects = self.pageQ.get_traced_objects_list(self.object)
        #     context['libraryitems'] = traced_objects['traced_sources']
        #     context['libraryitems_count'] = traced_objects['traced_sources_count']
        #     context['manuscripts'] = traced_objects['traced_manuscripts']
        #     context['manuscripts_count'] = traced_objects['traced_manuscripts_count']
        #     context['textlines'] = traced_objects['traced_novellines']
        #     context['textlines_count'] = traced_objects['traced_novellines_count']
        return context
