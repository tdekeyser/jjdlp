from django import forms
from haystack.forms import HighlightedModelSearchForm
from haystack.query import SearchQuerySet
from notebooks.models import Note

# class NoteSearchForm(HighlightedModelSearchForm):
#     '''Overrides the Haystack SearchForm for Note-only fast search box'''
#     models = [Note]

#     def get_models(self):
#     	return self.models

#     def search(self):
# 		sqs = super(NoteSearchForm, self).models(*self.get_models()).search()
# 		return sqs