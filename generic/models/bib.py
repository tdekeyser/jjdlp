'''
Abstract models for items that allow a fast bibliographic reference.
'''
from django.db import models

from generic.utils.bib import pybib


class Author(models.Model):
    '''
    Model for a text author. A separate model is needed in
    order to allow a ManyToMany relationship with the item.
    '''
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        if self.first_name:
            return u'{0}, {1}'.format(self.last_name, self.first_name)
        else:
            return u'{}'.format(self.last_name)

    class Meta:
        ordering = ['last_name']


class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        if self.city:
            return u'{0}: {1}'.format(self.city, self.name)
        else:
            return u'{}'.format(self.name)


class BibModel(models.Model):
    '''
    Abstract model that inherently generates a bibliographic reference.
    It is specifically aimed for items that need bibliographic references.
    These are automatically saved to the database.

    Getter methods allow different outputs for instance when parts of the
    bibliographic info is missing.
    '''
    title = models.CharField(max_length=300)
    item_type = models.CharField(max_length=10, blank=True)
    author = models.ManyToManyField(Author, blank=True)
    publisher = models.ForeignKey(Publisher, default='', blank=True, null=True)
    date = models.PositiveIntegerField(blank=True, null=True)
    # bibliographic reference field
    bib = models.TextField(blank=True)

    def __unicode__(self):
        return u'{}'.format(self.title)

    def save(self, *args, **kwargs):
        # override
        if not self.bib:
            # create bibliographic reference
            self.bib = pybib(self)
        super(BibModel, self).save(*args, **kwargs)

    # # getters
    def get_author(self):
        return u' & '.join([unicode(a) for a in self.author.all()])

    def get_title(self):
        return self.title

    def get_date(self):
        return self.date if self.date else '[n.d.]'

    def get_item_type(self):
        return self.item_type

    def get_publisher(self):
        return self.publisher

    class Meta:
        abstract = True
        ordering = ['date']
