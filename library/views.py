from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from haystack.forms import ModelSearchForm
from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

from library.models import Source, SourceCollection, SourcePage

class LibraryHomeView(TemplateView):
	template_name='library/library_base.html'

	def get_context_data(self, **kwargs):
		context = super(LibraryHomeView, self).get_context_data(**kwargs)

		context['virtual_library'] = SourceCollection.objects.get(slug='virtual-library')
		context['newspapercollections'] = SourceCollection.objects.filter(collection_type='newspaper')
		context['source_amount'] = Source.objects.count()
		context['vl_example'] = SourcePage.objects.filter(page_number__contains='frontcover').order_by('?').first() # random frontcover example (db small enough for this query)

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

class CollectionDetail(DetailView):
	'''DetailView of library collections; name=sourcecollection_detail'''
	model = SourceCollection

	def get_object(self, **kwargs):
		return self.model.objects.get(slug__exact=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super(CollectionDetail, self).get_context_data(**kwargs)

		items = self.object.item_of_collection.all()

		context['fromCollection'] = True
		context['collectionItems'] = items
		context['counted_items'] = items.count()
		context['frontcover'] = self.object.image

		return context

	def get_template_names(self, **kwargs):
		return 'library/source_detail.html'

class SourceDetail(DetailView):
	'''DetailView of library item; name=source_detail'''
	model = Source

	def get_context_data(self, **kwargs):
		'''Returns specific info as context for each page'''
		context = super(SourceDetail, self).get_context_data(**kwargs)

		context['fromSource'] = True

		images = self.object.page_of_source.get_all_images_but_frontcover() # all available images
		context['counted_items'] = images.count()
		context['coverimages'] = self.object.page_of_source.get_coverimages()
		try:
			context['frontcover'] = self.object.page_of_source.get_frontcover()
		except ObjectDoesNotExist:
			pass

		images_with_notes = self.object.page_of_source.get_detailimages()
		context['counted_images_with_notes'] = images_with_notes.count()
		context['images_with_notes'] = self.object.page_of_source.order_by_actualpagenumber(images_with_notes)

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
		page = SourcePage.objects.get(source=self.sourceitem, page_number__contains=self.kwargs['req_page'])
		return page

	def get_context_data(self, **kwargs):
		context = super(SourcePageDetail, self).get_context_data(**kwargs)

		try:
			context['frontcover'] = self.sourceitem.page_of_source.get_frontcover()
		except ObjectDoesNotExist:
			pass

		images = self.sourceitem.page_of_source.get_two_surroundingimages(self.kwargs['req_page'], needReordering=True)
		context['chosen_image'] = images['chosen_image']
		context['previous_image'] = images['previous_image']
		context['next_image'] = images['next_image']
		context['sourceitem'] = self.sourceitem

		# note info
		found_excerpts = self.object.sourcepage_excerpt.all()
		if found_excerpts:
			context['found_excerpts'] = found_excerpts
			context['counted_excerpts'] = found_excerpts.count()
		
		return context

