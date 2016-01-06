from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers
from library.models import Source, SourcePage, SourceExcerpt
from manuscripts.models import ManuscriptExcerpt
from novels.models import Line

class Notebook(models.Model):
	'''
	Basic Notebook model
	'''

	name = models.CharField(max_length=80, primary_key=True)
	info = models.TextField(max_length=1000, blank=True)
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

class NotebookPage(models.Model):
	'''
	NotebookPage model,
		linked to Notebook with ForeignKey,
		saves uploaded image to notebooks media folder,
		depends on PageQuerySet, a custom manager that provides specific page querysets like
			get_contentimages(), get_frontcover(), get_backcover()
	'''

	notebook = models.ForeignKey(Notebook, max_length=50, related_name='notebook_page')
	page_number = models.CharField(max_length=15, primary_key=True)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	image_caption = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return u'%s' % (self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.NotebookPageQuerySet)()

	class Meta:
		ordering = ['notebook']

class Note(models.Model):
	'''
	Note model,
		connects to NotebookPage and Notebook with ForeignKey,
		links to Source and SourcePage with ForeignKey,
		has coordinates of its reference on SourcePage
	'''

	# references within notebooks
	notepage = models.ForeignKey(NotebookPage, max_length=50, related_name='note_of_page', blank=True)
	noteb = models.ForeignKey(Notebook, max_length=80, related_name='note_of_book', blank=True, null=True)
	
	# note content
	notejj = models.CharField(max_length=250)
	msinfo = models.TextField(max_length=500, blank=True)
	annotation = models.TextField(max_length=2000, blank=True)
	ctransfer = models.CharField(max_length=30, blank=True)
	source_info = models.TextField(blank=True)

	# sourcetext reference field
	sourcepageexcerpt = models.ManyToManyField(SourceExcerpt, related_name='note_set', blank=True)
	# manuscript reference field; Joyce did not use a note twice --> ForeignKey
	manuscriptexcerpt = models.ForeignKey(ManuscriptExcerpt, related_name='note_set', blank=True, null=True)
	# novel reference field
	novelline = models.ForeignKey(Line, max_length=15, related_name='note_set', blank=True, null=True)

	def __unicode__(self):
		return u'{0} {1}'.format(self.notepage, self.notejj)

	def short(self):
		return u'{0}{1}'.format(self.notepage, self.notejj[:3])
