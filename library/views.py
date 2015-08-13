from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.template import RequestContext
from haystack.forms import ModelSearchForm
from haystack.views import SearchView
from library.models import Source, SourcePage
from library.forms import FastSearchForm

class LibraryHomeView(TemplateView):
	template_name='library/library_base.html'

	def get_context_data(self, **kwargs):
		context = super(LibraryHomeView, self).get_context_data(**kwargs)
		context['source_amount'] = Source.objects.count_sources()
		return context

class FastSearchView(SearchView):
	form = FastSearchForm
	template = 'library/search_results.html'

class SourceList_letter(ListView):
	'''View for ordering the list per field and per first letter'''
	context_object_name = 'sources'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		'''Adds context to template and changes name of the page_obj object (for pagination purposes)'''
		context = super(SourceList_letter, self).get_context_data(**kwargs)

		context['first_letter'] = self.kwargs['first_letter']
		context['source_field'] = self.kwargs['source_field']
		context['page'] = context['page_obj']
		del context['page_obj']
		return context

	def get_queryset(self, **kwargs):
		'''Sorts specified fields on the basis of the model method'''
		source_field = self.kwargs['source_field']
		letter = self.kwargs['first_letter']
		return Source.objects.field_sort(letter, source_field)

	def get_template_names(self, **kwargs):
		return 'library/source_list.html'

class SourceDetail(DetailView):
	'''View details of single source entry'''
	model = Source

	def get_context_data(self, **kwargs):
		'''Returns specific info as context for each page'''
		context = super(SourceDetail, self).get_context_data(**kwargs)

		context['coverimages'] = self.object.page_source.get_coverimages()

		context['tracedimages'] = self.object.page_source.order_by_actualpagenumber(self.object.page_source.get_contentimages())
		context['counted_tracedimages'] = self.object.page_source.count_contentimages()

		return context

	def get_template_names(self, **kwargs):
		return 'library/source_detail.html'

class SourcePageDetail(DetailView):
	'''View details of page'''
	model = Source

	def get_template_names(self, **kwargs):
		return 'library/source_detailed_page.html'

	def get_context_data(self, **kwargs):
		context = super(SourcePageDetail, self).get_context_data(**kwargs)

		context['frontcover'] = self.object.page_source.get_frontcover()

		images = self.object.page_source.get_allsurroundingimages(self.kwargs['req_page'])
		context['chosen_page'] = images['chosen_image']
		context['previous_pages'] = images['previous_images']
		context['next_pages'] = images['next_images']
		
		return context

