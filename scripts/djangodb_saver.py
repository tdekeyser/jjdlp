'''
Extract information from the notebook XML via SoupExtractor and save it to the notebook database.

******************* use of DjangoSqlSaver() and SoupExtractor() *********************

DjangoSqlSaver() depends on the file soupextractor.py in the folder py_classes; it creates an instance of SoupExtractor,
which takes as input the entire XML and returns a list of pages containing dictionaries with notes.

!!! SoupExtractor() is reliant on the tag definitions of the notebook XMLs. Other XMLs with other tags WILL NOT WORK !!!

To execute this file: start terminal; python manage.py shell; type execfile('path/to/djangodb_saver.py').
'''

import re
from scripts.py_classes.soupextractor import SoupExtractor
from django.utils.encoding import smart_str
from notebooks.models import Note, NotebookPage
from library.models import Source

class DjangoSqlSaver(object):
	def __init__(self):
		notebook_name = raw_input('Enter name of the notebook (don\'t forget the dot!):\n')
		if len(notebook_name)< 1: notebook_name = 'B.10'
		self.extraction = SoupExtractor()
		self.db_save()
		# self.db_save(self.extraction) is not needed i think; then following line was def db_save(self, extraction): --> also not needed

	def db_save(self):
		'''Save extracted pages to database'''
		for page in self.extraction:
			for note in page['page_list']:

				notejj = note['notejj0']
				annotation = note['annotation']
				msinfo = note['msinfo']
				ctransfer = note['ctransfer']
				source = note['source']

				new_note_object = Note(
					notejj = smart_str(notejj),
					annotation = smart_str(annotation),
					msinfo = smart_str(msinfo),
					ctransfer = smart_str(ctransfer),
					source_info = smart_str(source)
					)

				if not Note.objects.filter(notejj__icontains=smart_str(notejj)):
					if source:
						source_fragment = re.findall(r'^[^\d]+', source)[0].strip(',. ?!;:+')
						parent_source_object = Source.objects.filter(title__icontains=source_fragment)

						if parent_source_object:
							parent_source_object[0].source_note.add(new_note_object)

					parent_page_object = NotebookPage.objects.get(page_number=page['notebpage'])
					parent_page_object.note.add(new_note_object)

					new_note_object.save()
				else:
					print 'Did not save the following instance; it already appeared in the database: %s' % (notejj)
			print 'Finished saving to %s' % (page['notebpage'])

# Initiate class after starting the program
DjangoSqlSaver()
