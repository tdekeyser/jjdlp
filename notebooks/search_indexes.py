# rebuild_index or update_index

from haystack import indexes
from notebooks.models import Note

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	notejj_index = indexes.CharField(model_attr='notejj')
	note_sourceinfo = indexes.CharField(model_attr='source_info')

	def get_model(self):
		return Note

	def index_queryset(self, using=None):
		'''Used when entire index for model is updated.'''
		return self.get_model().objects.all()
