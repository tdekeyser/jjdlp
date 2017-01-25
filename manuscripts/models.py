from django.db import models

from library.models import LibraryItem, LibraryExcerpt
from texts.models import Text, Line

from gentext.models.structure import RecursiveCollectionModel, PageModel


def upload_to_collection(instance, filename):
    url = 'manuscripts/images/{0}/{1}'.format(instance.title, filename)
    return url


def upload_to_file(instance, filename):
    '''
    Defines where newly uploaded manuscript images should be saved.
    '''
    url = 'manuscripts/images/{0}/{1}'.format(instance.manuscript.title, filename)
    return url


class Manuscript(RecursiveCollectionModel):
    '''
    Basic model for a series of manuscripts
    '''
    note_on_transcriptions = models.TextField(blank=True)
    text = models.ForeignKey(Text, blank=True, null=True)
    # libraryitem = models.ManyToManyField(LibraryItem, blank=True)
    frontcover = models.ImageField(upload_to=upload_to_collection, blank=True)


class ManuscriptPage(PageModel):
    '''
    Basic model for a manuscript page
    '''
    manuscript = models.ManyToManyField(Manuscript, related_name="page_set", blank=True)
    jja = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to=upload_to_file, blank=True)
    numerical_order = models.PositiveSmallIntegerField()
    transcription = models.TextField(blank=True)    # contains XML
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['numerical_order']


class ManuscriptExcerpt(models.Model):
    '''
    A TranscriptionExcerpt is a piece of text within a transcription of which a note or sourcetext has been found.
    Defining it separately facilitates later manipulation of it.
    '''
    content = models.TextField()

    manuscript = models.ForeignKey(Manuscript, related_name='excerpt_set', blank=True, null=True)
    manuscriptpage = models.ForeignKey(ManuscriptPage, related_name='excerpt_set', blank=True)
    # reference fields to sourcepage
    librarypage = models.ManyToManyField(LibraryExcerpt, related_name='excerpt_set', blank=True)
    # reference to novelpage
    novelline = models.ManyToManyField(Line, related_name='excerpt_set', blank=True)
    # manuscript excerpt reference field
    manuscriptexcerpt = models.ForeignKey('self', on_delete=models.CASCADE, related_name='excerpt_set', blank=True, null=True)

    def __unicode__(self):
        return u'{0}...'.format(self.content[:30])
