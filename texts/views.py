from django.views.generic import TemplateView

from haystack.views import SearchView

from texts.models import Text, Line
from gentext.views.item import ItemView
from gentext.views.page import PageView


TEXTS_DUMMY_BASE = 'texts/dummy_base.html'


class TextsHomeView(TemplateView):
    template_name = 'texts/base.html'

    def get_context_data(self, **kwargs):
        context = super(TextsHomeView, self).get_context_data(**kwargs)
        context['linecount'] = Line.objects.count()
        context['textcount'] = Text.objects.count()
        context['texts'] = Text.objects.all()
        return context


class TextsSearchView(SearchView):
    template = 'texts/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=texts.line'}


class TextView(ItemView):
    model = Text
    slug_name = 'slug'
    template = 'texts/item.html'
    dummybase_template = TEXTS_DUMMY_BASE

    def sections(self):
        return self.item.section_set.all()

    def notebooks(self):
        return self.item.notebook_set.count()


class TextPageView(PageView):
    itemslug = 'slug'
    pageslug = 'page'

    parent_model = Text
    template = 'texts/page.html'
    dummybase_template = TEXTS_DUMMY_BASE

    def get_page(self):
        # override
        return self.pageQ.get(page_number=self.kwargs[self.pageslug])

    def get_context_data(self, **kwargs):
        # override
        context = super(TextPageView, self).get_context_data(**kwargs)
        context['lines'] = self.object.line_set.all()
        return context
