#apply models with python manage.py validate; then manage.py sqlall (model); then manage.py syncdb

from django.db import models
from library.models import Source
from library.managers import pagequery
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

class Notebook(models.Model):
	name = models.CharField(max_length=80, primary_key=True)
	info = models.TextField(max_length=1000, blank=True)
	further_usage = models.CharField(max_length=100, blank=True)
	used_source = models.ManyToManyField(Source, blank=True)

	def __unicode__(self):
		return u'%s' % (self.name)

	def get_usedsources(self):
		return ', '.join([u'%s' % x for x in self.used_source.all()])

class NotebookPage(models.Model):
	def upload_to_file(self, filename):
		url = 'notebooks/images/%s/%s' % (self.notebook_ref.name, filename)
		return url

	notebook_ref = models.ForeignKey(Notebook, max_length=50, related_name='notebook_page')
	page_number = models.CharField(max_length=15, primary_key=True)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	image_caption = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return u'%s' % (self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(pagequery.PageQuerySet)()

class Note(models.Model):
	notepage = models.ForeignKey(NotebookPage, max_length=50, related_name='note', blank=True)
	notejj = models.CharField(max_length=250)
	msinfo = models.TextField(max_length=500, blank=True)
	source = models.ForeignKey(Source, related_name='source_note', blank=True, null=True)
	source_info = models.TextField(max_length=2000, blank=True)
	annotation = models.TextField(max_length=2000, blank=True)
	ctransfer = models.CharField(max_length=30, blank=True)

	def __unicode__(self):
		return u'%s' % (self.notejj)

# class NoteSourceText(models.Model):
# create sourcetext class IN LIBRARY that links with notebook notes????

