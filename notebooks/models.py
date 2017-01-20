from django.db import models

from library.models import LibraryExcerpt, LibraryItem
from manuscripts.models import ManuscriptExcerpt
from texts.models import Text, Line

from gentext.models.structure import RecursiveCollectionModel, SlugModel, PageModel


def upload_to_file(instance, filename):
    '''
    Defines where newly uploaded notebook images should be saved.
    '''
    url = 'notebooks/images/{0}/{1}'.format(instance.notebook.name, filename)
    return url


class NotebookCollection(RecursiveCollectionModel):
    '''
    A basic collection model for a set of notebooks.
    '''
    pass


class Notebook(SlugModel):
    '''
    Basic Notebook model
    '''
    collection = models.ForeignKey(NotebookCollection, default='', related_name='item_set', blank=True)
    libraryitem = models.ManyToManyField(LibraryItem, related_name='notebook_set', blank=True)
    text = models.ForeignKey(Text, default='', related_name='notebook_set', blank=True)
    name = models.CharField(max_length=80, primary_key=True, verbose_name='title')
    item_type = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=255, blank=True)
    info = models.TextField(blank=True)
    draft_period = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.name)


class NotebookPage(PageModel):
    '''
    NotebookPage model,
        linked to Notebook with ForeignKey,
        saves uploaded image to notebooks media folder.
    '''
    notebook = models.ForeignKey(Notebook, max_length=50, related_name='page_set')
    image = models.ImageField(upload_to=upload_to_file, blank=True)

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
    # text reference field
    textline = models.ForeignKey(Line, max_length=255, related_name='note_set', blank=True, null=True)
    # note reference field
    note = models.ForeignKey('self', on_delete=models.CASCADE, related_name='note_set', blank=True, null=True)

    def __unicode__(self):
        return u'{0}{1}'.format(self.page, self.notejj[:3])

    def short(self):
        return u'{}'.format(self.notejj)

    class Meta:
        ordering = ['notejj']
