import re
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from haystack.forms import HighlightedModelSearchForm

from notebooks.models import Notebook, NotebookPage, Note


class NotebookHomeView(TemplateView):
	'''
	NOTEBOOKS_HOME presents:
		- short information on notebooks section
		- search functionality
		- a list of all available notebooks
		- amount of notebooks and notes
	'''
	
	template_name = 'notebooks/notebooks_base.html'

	def get_context_data(self, **kwargs):
		context = super(NotebookHomeView, self).get_context_data(**kwargs)
		context['notebooks'] = Notebook.objects.all()
		context['counted_notebooks'] = Notebook.objects.all().count()
		context['counted_notes'] = Note.objects.all().count()

		# notebook images
		context['b1frontcover'] = NotebookPage.objects.get(page_number__exact='B.1.a_frco')
		context['c_example'] = None
		context['d_example'] = None
		
		return context

class NoteSearchView(SearchView):
	form = HighlightedModelSearchForm
	template = 'notebooks/search_results.html'

	def extra_context(self, **kwargs):
		return {'specific_model': 'models=notebooks.note'}

class NotebookView(ListView):
	'''
	Passes context to NOTEBOOK_DETAIL:
		- frontcover
		- counts notebook pages and notes
		- paginates 4 notebook pages
	'''

	context_object_name = 'notebook_pages'
	paginate_by = 4

	def get_context_data(self, **kwargs):
		context = super(NotebookView, self).get_context_data(**kwargs)

		requested_notebook = Notebook.objects.get(name=self.kwargs['noteb'])

		try:
			context['cover'] = requested_notebook.notebook_page.get_frontcover()
			context['coverinfo'] = 'Front cover'
		except:
			try:
				context['cover'] = requested_notebook.notebook_page.get_backcover()
				context['coverinfo'] = 'Back cover'
			except:
				pass
			
		context['object'] = requested_notebook
		context['object_pages'] = requested_notebook.notebook_page.get_contentimages()
		context['counted_pages'] = requested_notebook.notebook_page.all().count()
		context['counted_notes'] = requested_notebook.note_of_book.all().count()
		context['page'] = context['page_obj']
		del context['page_obj']
		return context

	def get_queryset(self, **kwargs):
		return Notebook.objects.get(name=self.kwargs['noteb']).notebook_page.all()

	def get_template_names(self):
		return 'notebooks/notebook_detail.html'

class NotebookPageDetail(DetailView):
	'''
	NOTEBOOKPAGE_DETAIL,
		takes notebookpage as object,
		lists all notes on the page,
		provides detailed information on each note,
		allows easy navigation to other notebookpages.
	'''

	model = NotebookPage
	pk_url_kwarg = 'notebpage'

	def get_queryset(self, **kwargs):
		notebook_name = re.findall(r'^([A-Z].\d+)', self.kwargs['notebpage'])
		queryset = NotebookPage.objects.filter(notebook_ref=notebook_name[0])
		return queryset

	def get_template_names(self, **kwargs):
		return 'notebooks/notebookpage_detail.html'

	def get_context_data(self, **kwargs):
		context = super(NotebookPageDetail, self).get_context_data(**kwargs)

		notebook_obj = self.object.notebook_ref
		surrounding_images = notebook_obj.notebook_page.order_by('page_number').get_two_surroundingimages(self.kwargs['notebpage'])

		try:
			context['frontcover'] = notebook_obj.notebook_page.get_frontcover()
		except ObjectDoesNotExist:
			try:
				context['frontcover'] = notebook_obj.notebook_page.get_backcover()
			except ObjectDoesNotExist:
				pass

		context['page_obj'] = context['object']
		del context['object']
		context['object'] = notebook_obj
		context['previous_page'] = surrounding_images['previous_image']
		context['next_page'] = surrounding_images['next_image']
		context['c_pages'] = notebook_obj.notebook_page.get_contentimages()

		notes = self.object.note_of_page.all()
		if notes:
			context['notes'] = notes

			traced_objects = notebook_obj.notebook_page.get_traced_objects_list(self.object)
			context['set_of_sources'] = traced_objects['sources']
			context['sources_count'] = traced_objects['sources_count']
			context['set_of_novelpages'] = traced_objects['novelpages']
			context['novelpages_count'] = traced_objects['novelpages_count']
		
		return context
