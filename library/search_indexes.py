from haystack import indexes
from library.models import LibraryItem, LibraryExcerpt


class LibraryItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    collection = indexes.CharField(model_attr='collection')
    item_type = indexes.CharField(model_attr='item_type')

    def get_model(self):
        return LibraryItem

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class LibraryExcerptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    item = indexes.CharField(model_attr='item')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return LibraryExcerpt

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
