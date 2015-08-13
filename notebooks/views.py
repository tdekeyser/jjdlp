import re
from django.shortcuts import render
from notebooks.models import Notebook, NotebookPage
from django.views.generic import TemplateView, ListView, DetailView

class NotebookHomeView(TemplateView):
	template_name = 'notebooks/notebooks_base.html'

	def get_context_data(self, **kwargs):
		context = super(NotebookHomeView, self).get_context_data(**kwargs)
		context['notebooks'] = Notebook.objects.all()
		context['counted_notebooks'] = Notebook.objects.all().count()
		return context

class NotebookView(ListView):
	'''Detail notebook with listed pages'''
	context_object_name = 'notebook_pages'
	paginate_by = 5

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
		context['counted_pages'] = requested_notebook.notebook_page.all().count()
		context['page'] = context['page_obj']
		del context['page_obj']
		return context

	def get_queryset(self, **kwargs):
		return Notebook.objects.get(name=self.kwargs['noteb']).notebook_page.all()

	def get_template_names(self):
		return 'notebooks/notebook_detail.html'

class NotebookPageDetail(DetailView):
	'''Detail notebookpage, takes notebookpage as object'''
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
		except:
			try:
				context['frontcover'] = notebook_obj.notebook_page.get_backcover()
			except:
				pass

		context['page_obj'] = context['object']
		del context['object']
		context['object'] = notebook_obj
		context['previous_page'] = surrounding_images['previous_image']
		context['next_page'] = surrounding_images['next_image']
		context['c_pages'] = notebook_obj.notebook_page.get_contentimages()

		if self.object.note.all():
			context['notes'] = self.object.note.all()
		
		return context
