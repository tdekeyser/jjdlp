from haystack.utils import Highlighter
from django.utils.html import strip_tags

class NoTruncateNorEscapeHighlighter(Highlighter):
	'''Overrides Haystack Highlighter'''
	def highlight(self, text_block):
		
		# no strip_tags()
		if len(text_block) > 200:
			self.text_block = strip_tags(text_block)
		else:
			self.text_block = text_block

		highlight_locations = self.find_highlightable_words()
		start_offset, end_offset = self.find_window(highlight_locations)

		# no truncate at beginning
		if len(text_block) < 200: start_offset = 0

		return self.render_html(highlight_locations, start_offset, end_offset)