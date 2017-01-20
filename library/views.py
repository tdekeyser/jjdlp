from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from gentext.views.item import ItemView
from gentext.views.page import PageView
from gentext.views.collection import CollectionView

from library.models import LibraryItem, LibraryCollection, LibraryExcerpt

from cache_utils.decorators import cached

import json


LIBRARY_DUMMY_BASE = 'library/dummy_base.html'


# use make_data.invalidate() to reset
@cached(60*60*24)
def make_data():
    '''
    Set up item dataset for visualisation.
    EXPENSIVE calculation; needs to be cached.
    '''
    count = []
    names = []
    for c in LibraryCollection.objects.all():
        if c.collection_type == 'newspaper':
            newspapers = 0
            for item in c.item_set.all():
                newspapers += item.excerpt_set.count()
            if newspapers != 0:
                count.append(newspapers)
                names.append(c.slug)
        else:
            for i in c.item_set.all():
                icount = i.excerpt_set.count()
                if icount != 0:
                    count.append(icount)
                    names.append(i.slug)
    return count, json.dumps(names)


class LibraryHomeView(TemplateView):
    template_name = 'library/base.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryHomeView, self).get_context_data(**kwargs)

        context['itemcount'] = LibraryItem.objects.count()
        context['rtcount'] = LibraryExcerpt.objects.count()
        # get data for bar chart
        countdata, namedata = make_data()
        context['countdata'] = countdata
        context['namedata'] = namedata
        return context


class LibrarySearchView(SearchView):
    form = HighlightedModelSearchForm
    template = 'library/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=library.libraryitem'}


class LibraryCollectionView(CollectionView):
    paginate_by = 12

    model = LibraryCollection
    slug_name = 'collection'

    template = 'library/collection.html'
    dummybase_template = LIBRARY_DUMMY_BASE

    def get_context_data(self, **kwargs):
        # override
        context = super(LibraryCollectionView, self).get_context_data(**kwargs)
        context['child_objects'] = []
        for child in context['child_collections']:
            # pass each child collection together with their subcollections
            # and a sample of their items to template
            collections = child.collection_set.all()
            items = child.item_set.all()[:8]
            context['child_objects'].append((child, collections, items))
        return context


class LibraryItemView(ItemView):
    paginate_by = 8

    model = LibraryItem
    slug_name = 'item'

    template = 'library/item.html'
    dummybase_template = LIBRARY_DUMMY_BASE

    def get_queryset(self, **kwargs):
        # override
        query = super(LibraryItemView, self).get_queryset(**kwargs)
        return self.pageQ.order_by_actualpagenumber(query)

    def all_notebooks(self):
        return self.item.notebook_set.all()

    def all_reading_traces(self):
        return self.item.excerpt_set.count()


class LibraryPageView(PageView):
    parent_model = LibraryItem
    itemslug = 'item'
    pageslug = 'page'

    template = 'library/page.html'
    dummybase_template = LIBRARY_DUMMY_BASE

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
    slug_name = 'item'

    template = 'library/list.html'
    dummybase_template = LIBRARY_DUMMY_BASE

    def get_queryset(self, **kwargs):
        # override
        super(LibraryExcerptView, self).get_queryset(**kwargs)
        return LibraryExcerpt.objects.filter(item=self.item)
