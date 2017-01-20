'''
Abstract classes for the basic components of a group of texts:
collections, items, and pages.
'''
from django.db import models
from django.template.defaultfilters import slugify

from gentext.managers.queryset import PageQuerySet


def short(name):
    '''
    Returns shortened unicode string of input string.
    '''
    if len(name) > 19:
        return u'{}...'.format(name[:19])
    else:
        return u'{}'.format(name)


class RecursiveCollectionModel(models.Model):
    '''
    Recursive collection model. Instances can therefore
    contain both items and collections.

    Automatically saves a slugfield for the collection name.
    '''
    collection = models.ForeignKey('self', on_delete=models.CASCADE, related_name='collection_set', blank=True, null=True)
    title = models.CharField(max_length=300)
    info = models.TextField(blank=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.title)

    def short(self):
        return short(self.title)

    def get_parents(self):
        '''
        Return list of all parent collections
        '''
        c = self
        collections = []
        while isinstance(c.collection, RecursiveCollectionModel):
            collections.insert(0, c.collection)
            c = c.collection
        return collections

    def recurse(self):
        '''
        Get parent collections compiled as url, including itself.
        '''
        return '/'.join(c.slug for c in self.get_parents() + [self])

    def save(self, *args, **kwargs):
        # override
        if not self.slug:
            self.slug = slugify(' '.join(str(self).split()[:7]))
        super(RecursiveCollectionModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    '''
    Basic model for an item of any kind that automatically saves
    a slug from the model's unicode() method.
    '''
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # override
        if not self.slug:
            # create slug; take 7 first words
            self.slug = slugify(' '.join(str(self).split()[:7]))
        super(SlugModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PageModel(models.Model):
    '''
    Basic model for a text page, like the pages of a book. A specific
    page manager has been added that contains methods to get the book's
    front and back cover, and methods that are able to get previous
    and next objects.

    All methods are based on input in the page_number field. As it is
    a CharField, identifiers like "frontcover" are allowed and, in fact,
    recommended. Such CharField also allows double scanned pages to be
    documented as e.g. p. 1-2.

    Warning: the page_number field needs to be unique!
    '''
    page_number = models.CharField(max_length=50, primary_key=True)
    slug = models.SlugField(max_length=255, blank=True)

    # manager
    objects = PageQuerySet.as_manager()

    def __unicode__(self):
        return u'{}'.format(self.page_number)

    def save(self, *args, **kwargs):
        # create a slug
        if not self.slug:
            self.slug = slugify(self.page_number)
        super(PageModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
