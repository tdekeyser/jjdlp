from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers

from gentext.models.bib import BibModel
from gentext.models.structure import RecursiveCollectionModel, ItemModel


def upload_to_collection(instance, filename):
    url = 'library/images/{0}/{1}'.format(instance.slug, filename)
    return url


def upload_to_item(instance, filename):
    url = 'library/images/{0}/{1}'.format(instance.item.slug, filename)
    return url


def short(name):
    '''
    Returns shortened unicode string of input string.
    '''
    if len(name) > 19:
        return u'{}...'.format(name[:19])
    else:
        return u'{}'.format(name)


class LibraryCollection(RecursiveCollectionModel):
    '''
    Recursive collection model. Instances can therefore
    contain both items and collections.
    '''
    collection_type = models.CharField(max_length=50, blank=True)
    publication_period = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=upload_to_collection, blank=True)

    def short(self):
        return short(self.title)


class LibraryItem(BibModel, ItemModel):
    '''
    Model for virtual library items like books, articles, newspaper issues,
    poems, encyclopaedia entries etc. It contains bibliographic information
    as well as links to the full content of the item and information about
    the finder of the item.
    '''
    collection = models.ForeignKey(LibraryCollection, related_name='item_set', blank=True, null=True)
    discovered_by = models.CharField(max_length=300, blank=True)
    side_note = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)

    notebooks = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        if self.item_type == 'newspaper':
            return u'{0}, {1}'.format(
                self.collection,
                self.title
                )
        else:
            return u'{}'.format(self.title)

    def short(self):
        return short(self.title)

    # getters
    def get_collection(self):
        return self.collection


class LibraryPage(models.Model):
    '''
    Model for a scanned page.
    '''
    item = models.ForeignKey(LibraryItem, blank=True, null=True, related_name='page_set', max_length=255)
    image = models.ImageField(upload_to=upload_to_item, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    # unique page number in form "TITLE-AUTHOR,pagenumber"
    page_number = models.CharField(max_length=50, primary_key=True)
    # non-unique page number
    actual_pagenumber = models.CharField(max_length=50, blank=True)

    # manager
    objects = PassThroughManager.for_queryset_class(custom_managers.LibraryPageQuerySet)()

    class Meta:
        ordering = ['actual_pagenumber']

    def __unicode__(self):
        return u'{}'.format(self.actual_pagenumber)

    def save(self, *args, **kwargs):
        # create short page number and slug
        if not self.actual_pagenumber:
            self.actual_pagenumber = str(self.page_number.split(',')[1])
        if not self.slug:
            self.slug = slugify(self.page_number)
        super(LibraryPage, self).save(*args, **kwargs)


class LibraryExcerpt(models.Model):
    '''
    Model for transcribed fragments.
    '''
    content = models.TextField()

    item = models.ForeignKey(LibraryItem, related_name='excerpt_set')
    page = models.ForeignKey(LibraryPage, related_name='excerpt_set')

    class Meta:
        ordering = ['page']

    def __unicode__(self):
        return u'{0}...'.format(self.content[:30])
