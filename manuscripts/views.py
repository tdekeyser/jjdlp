from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from manuscripts.models import Manuscript, ManuscriptPage
from gentext.views.collection import CollectionView
from gentext.views.page import PageView


MANUSCRIPTS_DUMMY_BASE = 'manuscripts/dummy_base.html'


class ManuscriptsHomeView(TemplateView):
    template_name = 'manuscripts/base.html'

    def get_context_data(self, **kwargs):
        context = super(ManuscriptsHomeView, self).get_context_data(**kwargs)
        context['counted_manuscripts'] = Manuscript.objects.count()
        context['counted_pages'] = ManuscriptPage.objects.count()
        return context


class ManuscriptsSearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'manuscripts/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=manuscripts.manuscriptpage'}


class ManuscriptView(CollectionView):
    model = Manuscript
    slug_name = 'collection'

    template = 'manuscripts/collection.html'
    dummybase_template = MANUSCRIPTS_DUMMY_BASE

    target = ''

    def __init__(self, **kwargs):
        # override
        if kwargs['target'] == 'detail':
            self.paginate_by = 12
            self.template = 'manuscripts/collection.html'
        elif kwargs['target'] == 'pagelist':
            self.paginate_by = 10
            self.template = 'manuscripts/list.html'

    def set_page_caller(self):
        # override
        self.pageQ = self.get_item().page_set

    def get_context_data(self, **kwargs):
        # override
        context = super(ManuscriptView, self).get_context_data(**kwargs)
        context['all_pages'] = self.pages().all()
        context['child_objects'] = []
        for child in context['child_collections']:
            # pass each child collection together with their subcollections
            # and a sample of their items to template
            collections = child.collection_set.all()
            items = child.item_set.all()[:8]
            context['child_objects'].append((child, collections, items))
        return context


class ManuscriptPageView(PageView):
    parent_model = Manuscript
    itemslug = 'collection'
    pageslug = 'page'

    template = 'manuscripts/page.html'
    dummybase_template = MANUSCRIPTS_DUMMY_BASE
