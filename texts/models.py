from django.db import models
from django.utils.text import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers
from generic.managers.queryset import PageQuerySet


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

    def abbr(self):
        '''Create title abbreviation'''
        if self.slug == 'finnegans-wake':
            return 'FW'
        elif self.slug == 'ulysses':
            return 'U'


class BookSection(models.Model):
    '''
    Model for sections ("books") that are sometimes part of a novel.
    '''
    novel = models.ForeignKey(Novel, related_name='section_set')
    title = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    '''
    Model for novel chapters
    '''
    novel = models.ForeignKey(Novel)
    booksection = models.ForeignKey(BookSection, blank=True, null=True)

    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255, blank=True)

    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        if self.booksection:
            return u'{0}.{1}'.format(self.booksection, self.number)
        else:
            return u'{}'.format(self.number)

    def save(self, *args, **kwargs):
        # override save() to make a unique slug on save
        if not self.slug:
            if self.booksection:
                self.slug = slugify('{0}{1}'.format(self.booksection, self.number))
            else:
                self.slug = '{}'.format(self.number)
        super(Chapter, self).save(*args, **kwargs)


class Page(models.Model):
    '''
    Model for a novel page
    '''
    novel = models.ForeignKey(Novel)
    booksection = models.ForeignKey(BookSection, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, blank=True, null=True)

    page_number = models.PositiveSmallIntegerField()

    slug = models.SlugField(unique=True, max_length=50, blank=True)

    # manager
    objects = PassThroughManager.for_queryset_class(PageQuerySet)()

    def __unicode__(self):
        return '{0} {1}'.format(self.novel.abbr(), self.page_number)

    def note_is_present(self):
        return bool(self.note_set.count())

    def save(self, *args, **kwargs):
        # override save() to make a unique slug on save
        if not self.slug:
            self.slug = '{0}-{1}'.format(self.novel.abbr().lower(), self.page_number)
        super(Page, self).save(*args, **kwargs)


class Line(models.Model):
    '''
    Model for each line of the novel
    '''
    novel = models.ForeignKey(Novel, blank=True, null=True)
    booksection = models.ForeignKey(BookSection, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, blank=True, null=True)
    page = models.ForeignKey(Page, blank=True, null=True)

    linenumber = models.CharField(max_length=10, null=True)
    content = models.TextField(null=True)

    def __unicode__(self):
        return u'{0}\t{1}'.format(self.linenumber, self.content)
