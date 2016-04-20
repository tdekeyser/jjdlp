from haystack import indexes
from library.models import LibraryItem, LibraryExcerpt


class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    content_auto = indexes.EdgeNgramField(model_attr='verbose_source_name')

    def get_model(self):
        return LibraryItem

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class LibraryExcerptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    source = indexes.CharField(model_attr='source')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return LibraryExcerpt

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
