'''
Abstract classes for a collection and item.
'''
from django.db import models
from django.template.defaultfilters import slugify


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
        if not self.id:
            self.slug = slugify(' '.join(str(self).split()[:7]))
        super(RecursiveCollectionModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ItemModel(models.Model):
    info = models.TextField(blank=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # override
        if not self.id:
            # create slug; take 7 first words
            self.slug = slugify(' '.join(str(self).split()[:7]))
        super(ItemModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
