from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from haystack.forms import ModelSearchForm
from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from library.models import Source, SourcePage


class LibraryHomeView(TemplateView):
	template_name='library/library_base.html'

	def get_context_data(self, **kwargs):
		context = super(LibraryHomeView, self).get_context_data(**kwargs)

		context['source_amount'] = Source.objects.count()
		context['vl_example'] = SourcePage.objects.get(page_number__exact='CAU-MON,a_frco')

		return context

class LibrarySearchView(SearchView):
	form = HighlightedModelSearchForm
	template = 'library/search_results.html'

	def extra_context(self, **kwargs):
		return {'specific_model': 'models=library.source'}

class SourceListLetter(ListView):
	'''View for ordering library items per field + letter; name=order_all'''
	context_object_name = 'sources'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(SourceListLetter, self).get_context_data(**kwargs)

		context['first_letter'] = self.kwargs['first_letter']
		context['source_field'] = self.kwargs['source_field']

		# context key 'page_obj' changed for pagination purposes
		context['page'] = context['page_obj']
		del context['page_obj']
		return context

	def get_queryset(self, **kwargs):
		source_field = self.kwargs['source_field']
		letter = self.kwargs['first_letter']

		# sort on field+letter via Source's manager function
		return Source.objects.field_sort(letter, source_field)

	def get_template_names(self, **kwargs):
		return 'library/source_list.html'

class SourceDetail(DetailView):
	'''DetailView of library item; name=source_detail'''
	model = Source

	def get_context_data(self, **kwargs):
		'''Returns specific info as context for each page'''
		context = super(SourceDetail, self).get_context_data(**kwargs)

		context['coverimages'] = self.object.page_of_source.get_coverimages()

		context['tracedimages'] = self.object.page_of_source.order_by_actualpagenumber(self.object.page_of_source.get_contentimages())
		context['counted_tracedimages'] = self.object.page_of_source.get_contentimages().count()

		all_tracedimages = 0
		for bookitem in Source.objects.all():
			all_tracedimages += bookitem.page_of_source.get_contentimages().count()

		context['all_tracedimages'] = float(context['counted_tracedimages'])/float(all_tracedimages)

		return context

	def get_template_names(self, **kwargs):
		return 'library/source_detail.html'

class SourcePageDetail(DetailView):
	'''DetailView of item page; name=page_detail'''
	model = SourcePage
	sourceitem = None

	def get_template_names(self, **kwargs):
		return 'library/sourcepage_detail.html'

	def get_object(self, **kwargs):
		self.sourceitem = Source.objects.get(slug__exact=self.kwargs['itemslug'])
		page = SourcePage.objects.get(source_ref=self.sourceitem, page_number__contains=self.kwargs['req_page'])
		return page

	def get_context_data(self, **kwargs):
		context = super(SourcePageDetail, self).get_context_data(**kwargs)

		try:
			context['frontcover'] = self.sourceitem.page_of_source.get_frontcover()
		except ObjectDoesNotExist:
			pass

		images = self.sourceitem.page_of_source.get_allsurroundingimages(self.kwargs['req_page'])
		context['chosen_page'] = images['chosen_image']
		context['previous_pages'] = images['previous_images']
		context['next_pages'] = images['next_images']
		context['sourceitem'] = self.sourceitem

		# note info
		found_notes = self.object.note_on_sourcepage.all()
		if (found_notes):
			context['found_notes'] = found_notes
			context['counted_found_notes'] = found_notes.count()
		
		return context

