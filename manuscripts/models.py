from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers
from library.models import Source, SourceExcerpt
from novels.models import Novel, Page, Line

def upload_to_collection(instance, filename):
	url = 'manuscripts/images/{0}/{1}'.format(instance.title, filename)
	return url

class ManuscriptCollection(models.Model):
	'''
	Basic model for a series of manuscripts, i.e. the Red-backed Notebook or Haveth Childers Everywhere etc.
	'''
	title = models.CharField(max_length=100, primary_key=True)
	# perhaps use MARKDOWN for these info fields instead of pure HTML????
	homepage_info = models.TextField(blank=True)
	info = models.TextField(blank=True)
	note_on_transcriptions = models.TextField(blank=True)
	further_usage = models.ForeignKey(Novel, blank=True)
	used_source = models.ManyToManyField(Source, blank=True)
	frontcover = models.ImageField(upload_to=upload_to_collection, blank=True)

	'''Create slug'''
	slug = models.SlugField(unique=True, max_length=255, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(' '.join(self.title.split()[:7]))
		super(ManuscriptCollection, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'%s' % (self.title)

def upload_to_file(instance, filename):
	'''Defines where newly uploaded manuscript images should be saved.'''
	url = 'manuscripts/images/{0}/{1}'.format(instance.manuscript.title, filename)
	return url

class ManuscriptPageQueryset(custom_managers.PageQuerySet):
	'''Overrides the custom PageQuerySet'''
	def get_two_surroundingimages(self, req_page):
		'''Manuscript pages have been ordered by numerical_order field'''
		try:
			previous_image = self.filter(numerical_order__lt=req_page).reverse()[0]
		except IndexError:
			previous_image = ''

		try:
			next_image = self.filter(numerical_order__gt=req_page)[0]
		except IndexError:
			next_image = ''

		get_images = {
					'previous_image': previous_image,
					'next_image': next_image
				}

		return get_images

class ManuscriptPage(models.Model):
	'''
	Basic model for a manuscript page
	'''
	numerical_order = models.PositiveSmallIntegerField()
	manuscript = models.ForeignKey(ManuscriptCollection, max_length=100, related_name='manuscript_page')
	page_number = models.CharField(max_length=200, primary_key=True)
	jja = models.CharField(max_length=10, blank=True)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	image_caption = models.CharField(max_length=200, blank=True)

	transcription = models.TextField(blank=True) 	# contains XML
	specific_pageinfo = models.TextField(blank=True)

	'''Create slug'''
	slug = models.SlugField(unique=True, max_length=255, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.page_number)
		super(ManuscriptPage, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'{}'.format(self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(ManuscriptPageQueryset)()

	class Meta:
		ordering = ['numerical_order']

class ManuscriptExcerpt(models.Model):
	'''
	A TranscriptionExcerpt is a piece of text within a transcription of which a note or sourcetext has been found.
	Defining it separately facilitates later manipulation of it.
	'''
	content = models.TextField()

	manuscript = models.ForeignKey(ManuscriptCollection, related_name='excerpt_of_manuscriptcollection')
	manuscriptpage = models.ForeignKey(ManuscriptPage, related_name='excerpt_of_manuscriptpage')
	# reference fields to sourcepage
	sourcepage = models.ManyToManyField(SourceExcerpt, related_name='manuscriptexcerpt_set', blank=True)
	# reference to novelpage
	novelline = models.ManyToManyField(Line, related_name='manuscriptexcerpt_set', blank=True)

	# coordinates on page (x, y, width, height)
	x = models.PositiveSmallIntegerField(blank=True, null=True)
	y = models.PositiveSmallIntegerField(blank=True, null=True)
	w = models.PositiveSmallIntegerField(blank=True, null=True)
	h = models.PositiveSmallIntegerField(blank=True, null=True)
