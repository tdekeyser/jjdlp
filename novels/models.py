from django.db import models

class Novel(models.Model):
	'''
	Model for novel,
		has some simple information about a book.
		It does NOT allow searching by publisher (no ManyToManyField).
	'''

	title = models.CharField(max_length=50)
	# author is James Joyce by default; so no need for an author field
	publisher = models.CharField(max_length=255, blank=True)
	publication_date = models.PositiveSmallIntegerField(blank=True)
	slug = models.SlugField(unique=True, max_length=50, blank=True)
	info = models.TextField(max_length=1000, blank=True, null=True)

	def __unicode__(self):
		return self.title

class BookSection(models.Model):
	'''
	Model for sections ("books") that are sometimes part of a novel.
	'''

	novel = models.ForeignKey(Novel, related_name='section_in_novel', blank=True, null=True)
	title = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.title

class Chapter(models.Model):
	'''
	Model for novel chapters
	'''

	novel = models.ForeignKey(Novel, related_name='chapter_in_novel', blank=True, null=True)
	booksection = models.ForeignKey(BookSection, related_name='chapter_in_section', blank=True, null=True)

	number = models.PositiveSmallIntegerField()
	title = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return str(self.number)

class Page(models.Model):
	'''
	Model for a novel page
	'''

	novel = models.ForeignKey(Novel, related_name='page_of_novel', blank=True, null=True)
	booksection = models.ForeignKey(BookSection, related_name='page_of_section', blank=True, null=True)
	chapter = models.ForeignKey(Chapter, related_name='page_of_chapter', blank=True, null=True)

	pagenumber = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return str(self.pagenumber)

	def return_note_presence(self):
		return bool(self.note_of_novel.all())

class Line(models.Model):
	'''
	Model for each line of the novel
	'''

	novel = models.ForeignKey(Novel, related_name='line_of_novel', blank=True, null=True)
	booksection = models.ForeignKey(BookSection, related_name='line_of_section', blank=True, null=True)
	chapter = models.ForeignKey(Chapter, related_name='line_of_chapter', blank=True, null=True)
	page = models.ForeignKey(Page, related_name='line_of_page', blank=True, null=True)

	linenumber = models.CharField(max_length=10, null=True)
	content = models.TextField(null=True)

	def __unicode__(self):
		return u'{0}\t{1}'.format(self.linenumber, self.content)
