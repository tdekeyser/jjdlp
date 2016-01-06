from django.shortcuts import render
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, DetailView

from manuscripts.models import ManuscriptCollection, ManuscriptPage

from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

class ManuscriptsHomeView(TemplateView):
	'''
	MANUSCRIPTS_HOME presents:
		- information about collections ('home_info' field)
		- list of available collections
		- amount of collections etc.
	'''
	
	template_name = 'manuscripts/manuscripts_base.html'

	def get_context_data(self, **kwargs):
		context = super(ManuscriptsHomeView, self).get_context_data(**kwargs)
		context['manuscripts'] = ManuscriptCollection.objects.all()
		context['counted_manuscripts'] = ManuscriptCollection.objects.all().count()

		# manuscript images
		# context['red-backed_notebookcover'] = ManuscriptCollection.objects.get()
		
		return context

class ManuscriptsSearchView(SearchView):
	form = HighlightedModelSearchForm
	template = 'manuscripts/search_results.html'

	def extra_context(self, **kwargs):
		return {'specific_model': 'models=manuscripts.manuscriptpage'}

class ManuscriptCollectionView(ListView):
	context_object_name = 'manuscript_pages'

	def get_queryset(self, **kwargs):
		return ManuscriptCollection.objects.get(slug=self.kwargs['collectionslug']).manuscript_page.all()

	def get_context_data(self, **kwargs):
		context = super(ManuscriptCollectionView, self).get_context_data(**kwargs)

		collection = ManuscriptCollection.objects.get(slug=self.kwargs['collectionslug'])
		context['object'] = collection

		man_pages = collection.manuscript_page.all()
		context['counted_pages'] = man_pages.count()

		context['page'] = context['page_obj']
		del context['page_obj']

		try:
			context['frontcover'] = collection.frontcover
		except ObjectDoesNotExist:
			pass

		return context

class ManuscriptPageView(DetailView):
	model = ManuscriptCollection
	collection = None

	def get_template_names(self, **kwargs):
		return 'manuscripts/manuscriptpage_detail.html'

	def get_object(self, **kwargs):
		self.collection = self.model.objects.get(slug=self.kwargs['collectionslug'])
		page = self.collection.manuscript_page.get(slug=slugify(self.kwargs['manuscriptpage']))
		return page

	def get_context_data(self, **kwargs):
		context = super(ManuscriptPageView, self).get_context_data(**kwargs)

		context['page_obj'] = context['object']
		del context['object']
		context['object'] = self.collection
		context['collectionslug'] = self.collection.slug

		surrounding_images = self.collection.manuscript_page.order_by('numerical_order').get_two_surroundingimages(self.object.numerical_order)
		context['previous_page'] = surrounding_images['previous_image']
		context['next_page'] = surrounding_images['next_image']

		return context
