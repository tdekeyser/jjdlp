from django.views.generic import TemplateView
from django.contrib.admin.models import LogEntry

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from library.models import LibraryItem, LibraryCollection
from library.models import LibraryPage, LibraryExcerpt

from generic.views.item import ItemView
from generic.views.page import PageView
from generic.views.collection import CollectionView

import operator
import json
from cache_utils.decorators import cached

library_dummy_base = 'library/dummy_base.html'


@cached(60)
# use make_data.invalidate() to reset
def make_data():
    '''
    Set up item dataset for visualisation.
    EXPENSIVE calculation; needs to be cached.
    '''
    count = []
    names = []
    for p in LibraryItem.objects.all():
        count.append(p.page_set.count())
        names.append(p.slug)
    return count, json.dumps(names)


class LibraryHomeView(TemplateView):
    template_name = 'library/base.html'

    def get_recent_actions(self):
        return LogEntry.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super(LibraryHomeView, self).get_context_data(**kwargs)

        context['collections'] = LibraryCollection.objects.all()
        context['virtual_library'] = LibraryCollection.objects.get(slug='virtual-library')
        context['newspapercollections'] = LibraryCollection.objects.filter(collection_type='newspaper')
        context['source_amount'] = LibraryItem.objects.count()
        context['page_amount'] = LibraryPage.objects.count()
        # random frontcover example (db still small enough for this query)
        context['vl_example'] = LibraryPage.objects.filter(page_number__contains='frontcover').order_by('?').first()
        # recent actions module
        context['recent_actions'] = self.get_recent_actions()
        countdata, namedata = make_data()
        context['countdata'] = countdata
        context['namedata'] = namedata
        context['len_data'] = LibraryItem.objects.count()
        context['max_data'] = max(countdata)
        return context


class LibraryMacroView(TemplateView):
    template_name = 'library/macro.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryMacroView, self).get_context_data(**kwargs)
        countdata, namedata = make_data()
        countdata2 = [i*3 for i in countdata]
        context['countdata'] = countdata2
        context['namedata'] = namedata
        context['len_data'] = LibraryItem.objects.count()
        context['max_data'] = 350
        return context


class LibrarySearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'library/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=library.source'}


class LibraryCollectionView(CollectionView):
    paginate_by = 25

    model = LibraryCollection
    slug_name = 'slug'

    template = 'library/collection.html'
    dummybase_template = library_dummy_base


class LibraryItemView(ItemView):
    paginate_by = 0

    model = LibraryItem
    slug_name = 'slug'

    template = 'library/item.html'
    dummybase_template = library_dummy_base

    def get_queryset(self, **kwargs):
        # override
        query = super(LibraryItemView, self).get_queryset(**kwargs)
        return self.pageQ.order_by_actualpagenumber(query)

    def all_notebooks(self):
        return self.item.notebook_set.all()


class LibraryPageView(PageView):
    parent_model = LibraryItem
    itemslug = 'itemslug'
    pageslug = 'req_page'

    template = 'library/page.html'
    dummybase_template = library_dummy_base

    def get_page(self):
        # override
        return self.pageQ.get(actual_pagenumber=self.kwargs[self.pageslug])

    def get_context_data(self, **kwargs):
        # override
        context = super(LibraryPageView, self).get_context_data(**kwargs)
        # note info
        found_excerpts = self.object.excerpt_set.all()
        if found_excerpts:
            context['found_excerpts'] = found_excerpts
            context['counted_excerpts'] = found_excerpts.count()
        return context


class LibraryExcerptView(ItemView):
    context_object_name = 'excerpts'
    paginate_by = 10

    model = LibraryItem
    slug_name = 'slug'

    template = 'library/list.html'
    dummybase_template = library_dummy_base

    def get_queryset(self, **kwargs):
        # override
        super(LibraryExcerptView, self).get_queryset(**kwargs)
        return LibraryExcerpt.objects.filter(item=self.item)
