# rebuild_index or update_index

from haystack import indexes
from manuscripts.models import ManuscriptPage


class ManuscriptPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    page_number_index = indexes.CharField(model_attr='page_number')
    transcription = indexes.CharField(model_attr='transcription')

    def get_model(self):
        return ManuscriptPage

    def index_queryset(self, using=None):
        '''Used when entire index for model is updated.'''
        return self.get_model().objects.all()
