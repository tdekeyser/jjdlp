from django.shortcuts import render
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from haystack.utils import Highlighter
from haystack.forms import HighlightedModelSearchForm

class AdvancedSearchForm(HighlightedModelSearchForm):
	'''Overrides the Haystack form'''
	def search(self):
		sqs = super(FastSearchForm, self).search()
		return sqs

class AdvancedSearchView(SearchView):
	'''Overrides the Haystack view'''
	template = 'search/advanced_search.html'
	form = AdvancedSearchForm()
