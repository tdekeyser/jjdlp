from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from manuscripts.models import ManuscriptCollection
from gentext.views.item import ItemView
from gentext.views.page import PageView


MANUSCRIPTS_DUMMY_BASE = 'manuscripts/dummy_base.html'


class ManuscriptsHomeView(TemplateView):
    '''
    MANUSCRIPTS_HOME presents:
    - information about collections ('home_info' field)
    - list of available collections
    - amount of collections etc.
    '''
    def get_context_data(self, **kwargs):
        context = super(ManuscriptsHomeView, self).get_context_data(**kwargs)
        context['manuscripts'] = ManuscriptCollection.objects.all()
        context['counted_manuscripts'] = ManuscriptCollection.objects.all().count()

        return context

    def get_template_names(self, **kwargs):
        return 'manuscripts/base.html'


class ManuscriptsSearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'manuscripts/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=manuscripts.manuscriptpage'}


class ManuscriptCollectionView(ItemView):
    model = ManuscriptCollection
    slug_name = 'slug'

    target = ''
    template = ''
    dummybase_template = MANUSCRIPTS_DUMMY_BASE

    def __init__(self, **kwargs):
        # override
        if kwargs['target'] == 'detail':
            self.paginate_by = 8
            self.template = 'manuscripts/item.html'
        elif kwargs['target'] == 'pagelist':
            self.paginate_by = 10
            self.template = 'manuscripts/list.html'

    def all_pages(self):
        return self.pages().all()


class ManuscriptPageView(PageView):
    parent_model = ManuscriptCollection
    itemslug = 'slug'
    pageslug = 'page'

    template = 'manuscripts/page.html'
    dummybase_template = MANUSCRIPTS_DUMMY_BASE

    def get_pagenumber(self):
        # override
        return self.page.numerical_order
