'''
Upload a directory of images to the website database.

To execute this file: start terminal; python manage.py shell; type execfile('path/to/upload_images.py')
'''

import os, glob, ntpath
from django.core.files import File
from library.models import Source, SourcePage
from notebooks.models import NotebookPage, Notebook

class UploadImages(object):
	def __init__(self):
		model_info = self.get_modelinfo()
		self.chosen_model = model_info['chosen_model']
		self.parent_object = model_info['parent_object']
		self.chosen_parent_model = model_info['chosen_parent_model']

		folder_path = raw_input('Provide the path to your folder with images:')
		self.extension = raw_input('What is the extension of the images? [jpg, JPG, JPE] ')
		while self.extension not in ['jpg', 'JPG', 'JPE']:
			self.extension = raw_input('Please choose one of the available options? [jpg, JPG, JPE] ')

		self.upload_images(folder_path)

	def get_modelinfo(self):
		'''Questions the user for database relations.'''
		model_choice = raw_input('Enter the nature of your input [notebook/source]:')

		while True:
			if model_choice == 'notebook':
				chosen_model = NotebookPage
				chosen_parent_model = Notebook
				parent_name = raw_input('Provide the name of the notebook (do not forget the dot!):')

				try:
					return {
						'parent_object': Notebook.objects.get(name=parent_name),
						'chosen_model': chosen_model,
						'chosen_parent_model': chosen_parent_model,
					}

				except:
					parent_name = raw_input('The name you entered has not been found. Please correct your entry:')

			elif model_choice == 'source':
				chosen_model = SourcePage
				chosen_parent_model = Source
				parent_name = raw_input('Provide the title of the book/newspaper:')

				try:
					return {
						'parent_object': Source.objects.get(title__icontains=parent_name),
						'chosen_model': chosen_model,
						'chosen_parent_model': chosen_parent_model,
					}
				except:
					parent_name = raw_input('The name you entered has not been found. Please correct your entry:')


			else:
				model_choice = raw_input("Please respond with 'notebook' or 'source'.\n")


	def upload_images(self, folder_path):
		'''
		Links each file to defined model and page in the Django database.

		1. Associate newly created notebookpage instance with its parent notebook object.
		2. At this point, we need to fetch the notebookpage in question, whether newly created or already existent.
		3. If there is none, create an ImageField instance using additional arguments (name_of_the_file, read_file **'rb' added for Windows users**).
		'''
		for filename in glob.glob(os.path.join(folder_path, '*.' + self.extension)):
			new_page_object = self.chosen_model(
				page_number = os.path.splitext(ntpath.basename(filename))[0],
				)

			if new_page_object not in self.chosen_model.objects.all():
				'''1'''
				if self.chosen_parent_model == Notebook:
					self.parent_object.notebook_page.add(new_page_object)
				else:
					self.parent_object.page_source.add(new_page_object)
				new_page_object.save()

				print "Saved image to database:", new_page_object.page_number

			else:
				print "Image already appeared in database:", filename

			'''2'''
			working_page = self.chosen_model.objects.get(page_number=os.path.splitext(ntpath.basename(filename))[0])

			if not working_page.image:
				'''3'''
				working_page.image.save(str(os.path.split(filename)[1]), File(open(filename, 'rb')))
				working_page.save()

				print "Saved image to database."
			else:
				print "Image already appeared in database:", working_page.image.url


# Initiate class after starting the program
UploadImages()
