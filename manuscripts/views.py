from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from manuscripts.models import ManuscriptCollection
from generic.views.item import ItemView
from generic.views.page import PageView


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
        return 'manuscripts/manuscripts_base.html'


class ManuscriptsSearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'manuscripts/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=manuscripts.manuscriptpage'}


class ManuscriptCollectionView(ItemView):
    model = ManuscriptCollection
    slug_name = 'collectionslug'

    target = ''
    template = ''

    def __init__(self, **kwargs):
        # override
        if kwargs['target'] == 'detail':
            self.paginate_by = 8
            self.template = 'manuscripts/manuscripts_detail.html'
        elif kwargs['target'] == 'pagelist':
            self.paginate_by = 10
            self.template = 'manuscripts/manuscripts_pagelist.html'

    def get_context_data(self, **kwargs):
        # override
        context = super(ManuscriptCollectionView, self).get_context_data(**kwargs)
        # change page_obj to page for paginator html
        context['page'] = context['page_obj']
        del context['page_obj']
        return context

    def get_template_names(self, **kwargs):
        # override
        return self.template


class ManuscriptPageView(PageView):
    parent_model = ManuscriptCollection
    itemslug = 'collectionslug'
    pageslug = 'manuscriptpage'

    def get_template_names(self, **kwargs):
        # override
        return 'manuscripts/manuscriptpage_detail.html'

    def get_pagenumber(self):
        # override
        return self.page.numerical_order
