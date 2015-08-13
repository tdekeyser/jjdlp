from haystack import indexes
from library.models import Source

class SourceIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	source_title = indexes.CharField(model_attr='title', boost=1.2)
	source_author = indexes.CharField(model_attr='get_authors', boost=1.2)

	content_auto = indexes.EdgeNgramField(model_attr='verbose_source_name')

	def get_model(self):
		return Source

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

	# def prepare(self, obj):
	# 	'''Boost the whole model, so that it goes up in the entire search result'''
	# 	data = super(SourceIndex, self).prepare(obj)
	# 	data['boost'] = 1.1
	# 	return data
