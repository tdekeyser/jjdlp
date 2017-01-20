from django.db import models
from django.utils.text import slugify

from gentext.models.structure import SlugModel
from gentext.managers.queryset import PageQuerySet


class Text(SlugModel):
    '''
    Model for novel,
        has some simple information about a book.
        It does NOT allow searching by publisher (no ManyToManyField).
    '''
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=255, blank=True, default='James Joyce')
    publisher = models.CharField(max_length=255, blank=True)
    publication_date = models.PositiveSmallIntegerField(blank=True)
    info = models.TextField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def short(self):
        '''
        Create title abbreviation
        '''
        if self.title == 'Finnegans Wake':
            return 'FW'
        elif self.title == 'Ulysses':
            return 'U'


class Section(models.Model):
    '''
    Model for sections ("books") that are sometimes part of a novel.
    '''
    text = models.ForeignKey(Text, related_name='section_set')
    title = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    '''
    Model for novel chapters
    '''
    text = models.ForeignKey(Text)
    section = models.ForeignKey(Section, blank=True, null=True)

    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255, blank=True)

    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        if self.section:
            return u'{0}.{1}'.format(self.section, self.number)
        else:
            return u'{}'.format(self.number)

    def save(self, *args, **kwargs):
        # override save() to make a unique slug on save
        if not self.slug:
            if self.section:
                self.slug = slugify('{0}{1}'.format(self.booksection, self.number))
            else:
                self.slug = '{}'.format(self.number)
        super(Chapter, self).save(*args, **kwargs)


class Page(models.Model):
    '''
    Model for a text page
    '''
    text = models.ForeignKey(Text)
    section = models.ForeignKey(Section, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, blank=True, null=True)

    page_number = models.PositiveSmallIntegerField()

    slug = models.SlugField(unique=True, max_length=50, blank=True)

    # manager
    objects = PageQuerySet.as_manager()

    def __unicode__(self):
        return '{0} {1}'.format(self.text.short(), self.page_number)

    def save(self, *args, **kwargs):
        # override save() to make a unique slug on save
        if not self.slug:
            self.slug = '{0}-{1}'.format(self.text.short().lower(), self.page_number)
        super(Page, self).save(*args, **kwargs)


class Line(models.Model):
    '''
    Model for each line of a text
    '''
    text = models.ForeignKey(Text, blank=True, null=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, blank=True, null=True)
    page = models.ForeignKey(Page, blank=True, null=True)

    linenumber = models.CharField(max_length=10, null=True)
    content = models.TextField(null=True)

    def __unicode__(self):
        return u'{0}\t{1}'.format(self.linenumber, self.content)

    def short(self):
        return u'{0} {1}'.format(self.text.short(), self.linenumber)
