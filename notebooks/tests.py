# do python manage.py test notebooks

from django.test import TestCase
from notebooks.models import Notebook, NotebookPage
from notebooks.views import NotebookPageDetail

def create_notebook(name):
	return Notebook(name=name)

def create_notebookpage(notebook_ref, page_number):
	return NotebookPage(notebook_ref=notebook_ref, page_number=page_number)

class NotebookPageDetailViewTest(TestCase):
	def test_two_surrounding_images(self):
		notebook = create_notebook('B.10')
		notebook.save()

		page1 = create_notebookpage(notebook, 'B.10.001')
		page1.save()
		page2 = create_notebookpage(notebook, 'B.10.002')
		page2.save()
		page3 = create_notebookpage(notebook, 'B.10.003')
		page3.save()

		self.assertEqual(page1, notebook.notebook_page.get_two_surroundingimages('B.10.002')['previous_image'])
		self.assertEqual(page3, notebook.notebook_page.get_two_surroundingimages('B.10.002')['next_image'])
		self.assertEqual('', notebook.notebook_page.get_two_surroundingimages('B.10.001')['previous_image'])
