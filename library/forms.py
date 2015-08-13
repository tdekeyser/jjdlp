from django import forms
from haystack.forms import HighlightedModelSearchForm
from haystack.query import SearchQuerySet
from library.models import Source

# sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))

class FastSearchForm(HighlightedModelSearchForm):
    '''Overrides the Haystack SearchForm for Source-only fast search box'''
    searchqueryset = SearchQuerySet().models(Source)

    def no_query_found(self):
		return self.searchqueryset.all()
