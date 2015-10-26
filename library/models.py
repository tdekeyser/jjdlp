# changes in models are put into effect by calling $ python manage.py makemigrations ; and then $ python manage.py migrate

from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager
from JJDLP.managers import custom_managers

def get_model_fields(model):
	fields = []
	options = model._meta
	for field in sorted(options.concrete_fields + options.many_to_many + options.virtual_fields):
		fields.append(field.name)
	return fields

class Author(models.Model):
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=50, blank=True)

	def __unicode__(self):
		return u'%s, %s' % (self.last_name, self.first_name)

	class Meta:
		ordering = ['last_name']

class Publisher(models.Model):
	publisher_name = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=50, blank=True)

	def __unicode__(self):
		return u'%s: %s' % (self.city, self.publisher_name)

class Usage(models.Model):
	'''
	If present, gets section and title of the published work
	'''

	used_book = models.CharField(max_length=100)
	used_book_chapter = models.CharField(max_length=15, blank=True)

	def __unicode__(self):
		return u'%s \n %s' % (self.used_book, self.used_book_chapter)

class Source(models.Model):
	'''
	Fields for the sources:
		verbose_source_name is the complete stringified title,
		creates slug, used for all book urls, on new save,
		uses custom manager, SourceQuerySet, with specific 
	'''

	source_type = models.CharField(max_length=10, blank=True)
	info = models.TextField(max_length=1000, blank=True)
	title = models.CharField(max_length=300)
	author = models.ManyToManyField(Author, blank=True)
	publisher = models.ForeignKey(Publisher, blank=True, null=True)
	publication_date = models.PositiveSmallIntegerField()
	usage = models.ManyToManyField(Usage, blank=True)
	lib_type = models.CharField(max_length=10, blank=True)
	source_link = models.CharField(max_length=255, blank=True)
	certainty_info = models.TextField(max_length=500, blank=True)

	class Meta:
		ordering = ['title']

	'''Create slug'''
	slug = models.SlugField(unique=True, max_length=255, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			if ':' in str(self.title):
				self.slug = slugify(self.title.split(':')[0])

			else:
				self.slug = slugify(' '.join(self.title.split()[:7]))
		super(Source, self).save(*args, **kwargs)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.SourceQuerySet)()

	'''Methods'''
	def __unicode__(self):
		return u'%s' % (self.title)

	def verbose_source_name(self):
		if self.get_authors():
			return u'{0}. {1}. {2}. {3}.'.format(self.get_authors(), self.publication_date, self.title, self.publisher)
		else:
			return u'{0}. {1}. {2}'.format(self.title, self.publication_date, self.publisher)

	def get_authors(self):
		names = u' & '.join([u'%s %s' % (a.first_name, a.last_name) for a in self.author.all()])
		return names.strip()

	def get_usage(self):
		usages = u' & '.join([u'%s %s' % (u.used_book, u.used_book_chapter) for u in self.usage.all()])
		return usages

def upload_to_file(instance, filename):
	'''Defines where newly uploaded notebook images should be saved.'''
	url = 'library/images/%s/%s' % (instance.source_ref.slug, filename)
	return url

class SourcePage(models.Model):
	'''
	Fields for source pages,
		saves image to library media folder
	'''

	source_ref = models.ForeignKey(Source, blank=True, null=True, related_name='page_of_source', max_length=255)
	page_number = models.CharField(max_length=20, primary_key=True)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	image_caption = models.CharField(max_length=200)

	actual_pagenumber = models.CharField(max_length=10, blank=True)

	width = models.PositiveSmallIntegerField(blank=True, null=True)
	height = models.PositiveSmallIntegerField(blank=True, null=True)

	def save(self, *args, **kwargs):
		self.actual_pagenumber = str(self.page_number.split(',')[1])
		super(SourcePage, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'%s' % (self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.PageQuerySet)()

	class Meta:
		ordering = ['source_ref']
		verbose_name = 'Source page'
		verbose_name_plural = 'Source pages'
