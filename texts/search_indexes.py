from haystack import indexes
from texts.models import Line


class LineIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    line_index = indexes.CharField(model_attr='content')

    def get_model(self):
        return Line

    def index_queryset(self, using=None):
        '''Used when entire index for model is updated.'''
        return self.get_model().objects.all()
