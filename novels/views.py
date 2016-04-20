from django.views.generic import TemplateView, DetailView
from django.core.paginator import Paginator

from haystack.views import SearchView

from novels.models import Novel, Line


class NovelsHomeView(TemplateView):
    template_name = 'novels/novels_base.html'

    def get_context_data(self, **kwargs):
        context = super(NovelsHomeView, self).get_context_data(**kwargs)

        context['lines'] = Line.objects.all().count()
        context['books'] = Novel.objects.all()
        return context


class NovelsSearchView(SearchView):
    template = 'novels/search_results.html'

    def extra_context(self, **kwargs):
        return {'specific_model': 'models=novels.line'}


class NovelDetailView(DetailView):
    model = Novel
    pk_url_kwarg = 'novelslug'

    def get_object(self, **kwargs):
        return Novel.objects.get(slug = self.kwargs['novelslug'])

    def get_template_names(self, **kwargs):
        return 'novels/novels_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NovelDetailView, self).get_context_data(**kwargs)
        pages = self.object.page_of_novel.all()

        context['sections'] = self.object.section_in_novel.all()
        context['pages'] = pages
        context['amountofpages'] = pages.count()
        context['amountoflines'] = self.object.line_of_novel.all().count()
        return context


class NovelPageView(DetailView):
    model = Novel
    novel = None

    def get_template_names(self, **kwargs):
        return 'novels/novelpage_detail.html'

    def get_object(self, **kwargs):
        self.novel = self.model.objects.get(slug=self.kwargs['novelslug'])
        page = self.novel.page_of_novel.get(pagenumber=self.kwargs['novelpage'])
        return page

    def get_context_data(self, **kwargs):
        context = super(NovelPageView, self).get_context_data(**kwargs)

        context['novelslug'] = self.novel.slug
        context['lines'] = self.object.line_of_page.all()

        paginator = Paginator(self.novel.page_of_novel.all(), 1)
        context['paginator'] = paginator.page(int(self.kwargs['novelpage'])-2)

        return context
