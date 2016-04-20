from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import PassThroughManager

from JJDLP.managers import custom_managers


def upload_to_collection(instance, filename):
    url = 'library/images/{0}/{1}'.format(instance.slug, filename)
    return url


def upload_to_item(instance, filename):
    url = 'library/images/{0}/{1}'.format(instance.item.slug, filename)
    return url


class Author(models.Model):

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return u'{0}, {1}'.format(self.last_name, self.first_name)

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


class LibraryCollection(models.Model):

    title = models.CharField(max_length=300)
    collection_type = models.CharField(max_length=50, blank=True)
    info = models.TextField(blank=True)
    publication_period = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=upload_to_collection, blank=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if ':' in str(self.title):
                self.slug = slugify(self.title.split(':')[0])
            else:
                self.slug = slugify(' '.join(self.title.split()[:7]))
        super(LibraryCollection, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.title)

    class Meta:
        ordering = ['title']


class LibraryItem(models.Model):

    title = models.CharField(max_length=300)
    item_type = models.CharField(max_length=10, blank=True)
    collection = models.ForeignKey(LibraryCollection, related_name='item_set', blank=True, null=True)
    author = models.ManyToManyField(Author, blank=True)
    publisher = models.ForeignKey(Publisher, default='', blank=True, null=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)
    info = models.TextField(blank=True)
    # link to external site, i.e. UA library or archive.org
    link = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # override save() to make slug on save
    def save(self, *args, **kwargs):
        if not self.id:
            # take 7 first words
            self.slug = slugify(' '.join(str(self).split()[:7]))
        super(LibraryItem, self).save(*args, **kwargs)

    # manager
    objects = PassThroughManager.for_queryset_class(custom_managers.SourceQuerySet)()

    def __unicode__(self):
        if self.item_type != 'book':
            return u'{0}, {1}'.format(
                self.collection,
                self.title
                )
        else:
            return u'{}'.format(self.title)

    def biblio(self):
        # return bibliographic info
        if self.get_authors():
            return u'{0}. {1}. {2}. {3}.'.format(
                self.get_authors(),
                self.date,
                self.title,
                self.publisher
                )
        else:
            return u'{0}. {1}. {2}'.format(
                self.title,
                self.date,
                self.publisher
                )

    def get_authors(self):
        names = u' & '.join([u'{0} {1}'.format(a.first_name, a.last_name) for a in self.author.all()])
        return names.strip()

    class Meta:
        ordering = ['title']


class LibraryPage(models.Model):

    item = models.ForeignKey(LibraryItem, blank=True, null=True, related_name='page_set', max_length=255)
    image = models.ImageField(upload_to=upload_to_item, blank=True)
    # unique page number in form "TITLE-AUTHOR,pagenumber"
    page_number = models.CharField(max_length=50, primary_key=True)
    # non-unique page number
    actual_pagenumber = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        self.actual_pagenumber = str(self.page_number.split(',')[1])
        super(LibraryPage, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.page_number)

    # manager
    objects = PassThroughManager.for_queryset_class(custom_managers.LibraryPageQuerySet)()

    class Meta:
        ordering = ['page_number']


class LibraryExcerpt(models.Model):
    '''
    Model for the traced fragments of the library items
    Place set to:
    * top-single / bottom-single
    * top-left / top-right / bottom-left / bottom-right
    '''
    content = models.TextField()

    item = models.ForeignKey(LibraryItem, related_name='excerpt_set')
    page = models.ForeignKey(LibraryPage, related_name='excerpt_set')

    # coordinates on page (x, y, width, height)
    x = models.PositiveSmallIntegerField(blank=True, null=True)
    y = models.PositiveSmallIntegerField(blank=True, null=True)
    w = models.PositiveSmallIntegerField(blank=True, null=True)
    h = models.PositiveSmallIntegerField(blank=True, null=True)
    # place on the page
    place = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return '{0}|{1}'.format(self.page, self.id)

    def short(self):
        return u'{0}...'.format(self.content[:30])

    class Meta:
        ordering = ['page']
