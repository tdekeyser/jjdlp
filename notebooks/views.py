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
		context['b1frontcover'] = NotebookPage.objects.filter(page_number__contains='frontcover').order_by('?').first()
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
		except ObjectDoesNotExist:
			try:
				context['cover'] = requested_notebook.notebook_page.get_backcover()
			except ObjectDoesNotExist:
				pass
			
		context['object'] = requested_notebook
		context['object_pages'] = requested_notebook.notebook_page.get_all_images_but_frontcover()
		context['counted_pages'] = requested_notebook.notebook_page.all().count()
		context['counted_notes'] = requested_notebook.note_of_book.all().count()
		context['page'] = context['page_obj']
		del context['page_obj']
		return context

	def get_queryset(self, **kwargs):
		notebook_name = re.sub(r'[.][0]', '.', self.kwargs['noteb'])
		return Notebook.objects.get(name=notebook_name).notebook_page.all()

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
		queryset = NotebookPage.objects.filter(notebook=self.kwargs['noteb'])
		return queryset

	def get_template_names(self, **kwargs):
		return 'notebooks/notebookpage_detail.html'

	def get_context_data(self, **kwargs):
		context = super(NotebookPageDetail, self).get_context_data(**kwargs)

		notebook_obj = self.object.notebook
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
		context['c_pages'] = notebook_obj.notebook_page.get_detailimages()

		notes = self.object.note_of_page.all()
		if notes:
			context['notes'] = notes

			traced_objects = notebook_obj.notebook_page.get_traced_objects_list(self.object)
			context['traced_sources'] = traced_objects['traced_sources']
			context['traced_sources_count'] = traced_objects['traced_sources_count']
			context['traced_manuscripts'] = traced_objects['traced_manuscripts']
			context['traced_manuscripts_count'] = traced_objects['traced_manuscripts_count']
			context['traced_novellines'] = traced_objects['traced_novellines']
			context['traced_novellines_count'] = traced_objects['traced_novellines_count']
		
		return context
