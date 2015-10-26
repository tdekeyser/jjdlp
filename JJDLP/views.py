'''
Interesting notes on setting up Haystack + Elasticsearch: https://gist.github.com/ramirezg/00d02ba2cbe85d522dfd
'''
from django.views.generic import TemplateView

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedModelSearchForm, ModelSearchForm

from notebooks.models import Note
from library.models import Source
from novels.models import Page

class AdvancedSearchView(SearchView):
	'''Overrides the Haystack view'''
	template = 'search/advanced_search.html'
	form = HighlightedModelSearchForm()

class StatsView(TemplateView):
	template_name = 'JJDLP/JJDLP_stats.html'

	def get_context_data(self, **kwargs):
		context = super(StatsView, self).get_context_data(**kwargs)

		context['library_items'] = Source.objects.all().count()
		context['notebooks_notes'] = Note.objects.all().count()
		context['novels_pages'] = Page.objects.all().count()

		return context
