from django.views.generic import TemplateView
from django.core.paginator import Paginator

from haystack.views import SearchView

from texts.models import Novel, Line
from gentext.views.item import ItemView
from gentext.views.page import PageView


NOVELS_DUMMY_BASE = 'texts/dummy_base.html'


class NovelsHomeView(TemplateView):
    template_name = 'texts/base.html'

    def get_context_data(self, **kwargs):
        context = super(NovelsHomeView, self).get_context_data(**kwargs)
        context['lines'] = Line.objects.count()
        context['books'] = Novel.objects.all()
        return context


class NovelsSearchView(SearchView):
    template = 'texts/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=texts.line'}


class NovelView(ItemView):
    model = Novel
    slug_name = 'slug'
    template = 'texts/item.html'
    dummybase_template = NOVELS_DUMMY_BASE

    def sections(self):
        return self.item.section_set.all()

    def amount_of_lines(self):
        return self.item.line_set.count()


class NovelPageView(PageView):
    itemslug = 'slug'
    pageslug = 'page'

    parent_model = Novel
    template = 'texts/page.html'

    def get_page(self):
        # override
        return self.pageQ.get(page_number=self.kwargs[self.pageslug])

    def get_context_data(self, **kwargs):
        # override
        context = super(NovelPageView, self).get_context_data(**kwargs)
        context['lines'] = self.object.line_set.all()
        paginator = Paginator(self.item.page_set.all(), 1)
        context['paginator'] = paginator.page(int(self.kwargs['page'])-2)
        return context
