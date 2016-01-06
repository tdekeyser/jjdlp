'''
Database models for the library module
'''

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers
from novels.models import Novel

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
		if self.city:
			return u'{0}: {1}'.format(self.city, self.publisher_name)
		else:
			return u'{}'.format(self.publisher_name)

def upload_to_collection(instance, filename):
	'''Defines where newly uploaded notebook images should be saved.'''
	url = 'library/images/{0}/{1}'.format(instance.slug, filename)
	return url

class SourceCollection(models.Model):
	'''
	Model for collections that gather multiple sources, e.g. newspapers.
	'''
	title = models.CharField(max_length=300)
	collection_type = models.CharField(max_length=50, blank=True)
	info = models.TextField(blank=True)
	publication_period = models.CharField(max_length=100, blank=True)
	image = models.ImageField(upload_to=upload_to_collection, blank=True)

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
		super(SourceCollection, self).save(*args, **kwargs)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.SourceQuerySet)()

	'''Methods'''
	def __unicode__(self):
		return u'%s' % (self.title)

class Source(models.Model):
	'''
	Fields for the sources:
		Verbose_source_name is the complete stringified title;
		Creates slug, used for all book urls, on new save;
		Uses custom manager, SourceQuerySet, with specific query methods
	'''

	source_type = models.CharField(max_length=10, blank=True)		# i.e. book, newspaper, etc.
	info = models.TextField(blank=True)								# specific source info for detail page
	collection = models.ForeignKey(SourceCollection, related_name='item_of_collection', blank=True, null=True)
	title = models.CharField(max_length=300)
	author = models.ManyToManyField(Author, blank=True)
	publisher = models.ForeignKey(Publisher, blank=True, null=True)
	publication_date = models.PositiveSmallIntegerField()
	usage = models.ManyToManyField(Novel, blank=True) 				# item used for these novels
	lib_type = models.CharField(max_length=10, blank=True)			# virtual or extant library
	source_link = models.CharField(max_length=255, blank=True)		# link to external site, i.e. UA library or archive.org
	certainty_info = models.TextField(max_length=500, blank=True)	# certainty measure that this source has been used

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
		'''Returns complete bibliographic information of the item as String'''
		if self.get_authors():
			return u'{0}. {1}. {2}. {3}.'.format(self.get_authors(), self.publication_date, self.title, self.publisher)
		else:
			return u'{0}. {1}. {2}'.format(self.title, self.publication_date, self.publisher)

	def get_authors(self):
		names = u' & '.join([u'%s %s' % (a.first_name, a.last_name) for a in self.author.all()])
		return names.strip()

def upload_to_file(instance, filename):
	'''Defines where newly uploaded notebook images should be saved.'''
	url = 'library/images/{0}/{1}'.format(instance.source.slug, filename)
	return url

class SourcePage(models.Model):
	'''
	Fields for source pages,
		saves image to library media folder
	'''

	source = models.ForeignKey(Source, blank=True, null=True, related_name='page_of_source', max_length=255)
	image = models.ImageField(upload_to=upload_to_file, blank=True)
	
	page_number = models.CharField(max_length=50, primary_key=True)		# unique page number in form "TITLE-AUTHOR,pagenumber"
	actual_pagenumber = models.CharField(max_length=50, blank=True)		# non-unique page number in form "pagenumber"

	def save(self, *args, **kwargs):
		self.actual_pagenumber = str(self.page_number.split(',')[1])
		super(SourcePage, self).save(*args, **kwargs)

	def __unicode__(self):
		return u'{}'.format(self.page_number)

	'''Manager'''
	objects = PassThroughManager.for_queryset_class(custom_managers.LibraryPageQuerySet)()

	class Meta:
		ordering = ['source']

class SourceExcerpt(models.Model):
	'''
	Model for the traced fragments of the library items
	'''
	content = models.TextField()

	source = models.ForeignKey(Source, related_name='source_excerpt')
	sourcepage = models.ForeignKey(SourcePage, related_name='sourcepage_excerpt')

	# coordinates on page (x, y, width, height)
	x = models.PositiveSmallIntegerField(blank=True, null=True)
	y = models.PositiveSmallIntegerField(blank=True, null=True)
	w = models.PositiveSmallIntegerField(blank=True, null=True)
	h = models.PositiveSmallIntegerField(blank=True, null=True)
	# place on the page
	place = models.CharField(max_length=20, blank=True)

	def __unicode__(self):
		return '{0}; "...{1}..."'.format(self.sourcepage.page_number, self.content[-30:])

	def short(self):
		return '...{0}...'.format(self.content[:30])
