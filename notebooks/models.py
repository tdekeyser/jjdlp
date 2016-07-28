from django.db import models
from model_utils.managers import PassThroughManager
from django.template.defaultfilters import slugify

from JJDLP.managers import custom_managers
from library.models import LibraryExcerpt, LibraryItem
from manuscripts.models import ManuscriptExcerpt
from texts.models import Line

from generic.managers.queryset import PageQuerySet


def upload_to_file(instance, filename):
    '''Defines where newly uploaded notebook images should be saved.'''
    url = 'notebooks/images/{0}/{1}'.format(instance.notebook.name, filename)
    return url


class Notebook(models.Model):
    '''
    Basic Notebook model
    '''
    name = models.CharField(max_length=80, primary_key=True, verbose_name='title')
    info = models.TextField(max_length=1000, blank=True)
    item_type = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=255, blank=True)
    draft_period = models.CharField(max_length=255, blank=True)
    libraryitem = models.ManyToManyField(LibraryItem, related_name='notebook_set', blank=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # override save() to make slug on save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Notebook, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.name)


class NotebookPage(models.Model):
    '''
    NotebookPage model,
        linked to Notebook with ForeignKey,
        saves uploaded image to notebooks media folder,
        depends on PageQuerySet, a custom manager that provides specific page querysets like
            get_contentimages(), get_frontcover(), get_backcover()
    '''
    notebook = models.ForeignKey(Notebook, max_length=50, related_name='page_set')
    page_number = models.CharField(max_length=255, primary_key=True)
    image = models.ImageField(upload_to=upload_to_file, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    # override save() to make slug on save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.page_number)
        super(NotebookPage, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.page_number)

    # manager
    objects = PassThroughManager.for_queryset_class(PageQuerySet)()

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
    page = models.ForeignKey(NotebookPage, max_length=100, verbose_name='page', related_name='note_set', blank=True)
    noteb = models.ForeignKey(Notebook, max_length=80, related_name='note_set', blank=True, null=True)

    # note content
    notejj = models.CharField(max_length=250)
    msinfo = models.TextField(max_length=500, blank=True)
    annotation = models.TextField(max_length=2000, blank=True)
    ctransfer = models.CharField(max_length=30, blank=True)
    source = models.TextField(blank=True)
    textref = models.CharField(max_length=50, blank=True)

    # library reference field
    libraryexcerpt = models.ManyToManyField(LibraryExcerpt, related_name='note_set', blank=True)
    # manuscript reference field; Joyce did not use a note twice --> ForeignKey
    manuscriptexcerpt = models.ForeignKey(ManuscriptExcerpt, related_name='note_set', blank=True, null=True)
    # novel reference field
    textline = models.ForeignKey(Line, max_length=255, related_name='note_set', blank=True, null=True)

    def __unicode__(self):
        return u'{0}{1}'.format(self.page, self.notejj[:3])

    def short(self):
        return u'{}'.format(self.notejj)

    class Meta:
        ordering = ['notejj']
