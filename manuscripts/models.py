from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers
from library.models import Source, SourcePage
from novels.models import Page
from notebooks.models import Note

class ManuscriptCollection(models.Model):
	'''
	Basic Manuscript model
	'''

	title = models.CharField(max_length=80, primary_key=True)
	info = models.TextField(max_length=2500, blank=True)
	further_usage = models.CharField(max_length=100, blank=True)
	used_source = models.ManyToManyField(Source, blank=True)

	def __unicode__(self):
		return u'%s' % (self.name)

	def get_usedsources(self):
		return ', '.join([u'%s' % x for x in self.used_source.all()])

def upload_to_file(instance, filename):
	'''Defines where newly uploaded notebook images should be saved.'''
	url = 'notebooks/images/%s/%s' % (instance.notebook_ref.name, filename)
	return url

class ManuscriptPage(models.Model):
	'''
	NotebookPage model,
		linked to Notebook with ForeignKey,
		saves uploaded image to notebooks media folder,
		depends on PageQuerySet, a custom manager that provides specific page querysets like
			get_contentimages(), get_frontcover(), get_backcover()
	'''

	notebook_ref = models.ForeignKey(Notebook, max_length=50, related_name='notebook_page')
	page_number = models.CharField(max_length=15, primary_key=True)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	image_caption = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return u'%s' % (self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.PageQuerySet)()

class Note(models.Model):
	'''
	Note model,
		connects to NotebookPage and Notebook with ForeignKey,
		links to Source and SourcePage with ForeignKey,
		has coordinates of its reference on SourcePage
	'''

	notepage = models.ForeignKey(NotebookPage, max_length=50, related_name='note_of_page', blank=True)
	noteb = models.ForeignKey(Notebook, max_length=80, related_name='note_of_book', blank=True, null=True)
	
	notejj = models.CharField(max_length=250)
	msinfo = models.TextField(max_length=500, blank=True)
	annotation = models.TextField(max_length=2000, blank=True)
	ctransfer = models.CharField(max_length=30, blank=True)

	# novel reference fields
	novelpage = models.CharField(max_length=50, blank=True, null=True)
	novelpage_ref = models.ForeignKey(Page, max_length=15, related_name='note_of_novel', blank=True, null=True)

	# sourcetext reference fields
	source = models.ForeignKey(Source, related_name='source_of_note', blank=True, null=True)
	source_info = models.TextField(max_length=2000, blank=True)

	source_page_ref = models.ForeignKey(SourcePage, related_name='note_on_sourcepage', blank=True, null=True)
	# coordinates for sourcepage reference
	x_on_sourcepage = models.PositiveSmallIntegerField(blank=True, null=True)
	y_on_sourcepage = models.PositiveSmallIntegerField(blank=True, null=True)
	width_on_sourcepage = models.PositiveSmallIntegerField(blank=True, null=True)
	height_on_sourcepage = models.PositiveSmallIntegerField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.notejj)

