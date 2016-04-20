from django import template
import markdown

register = template.Library()

@register.filter
def markdownify(text):
	# safe_mode governs how the function handles raw HTML + creates anchors to headers with table-of-contents extension
	md = markdown.Markdown(extensions=['markdown.extensions.toc'], safe_mode='escape') 
	return md.convert(text)
