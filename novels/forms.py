from haystack.forms import HighlightedModelSearchForm

class NovelsSearchForm(HighlightedModelSearchForm):
	def __init__(self, *args, **kwargs):
		super(NovelsSearchForm, self).__init__(*args, **kwargs)
		del self.fields['models']
		self.fields['models'] = None
