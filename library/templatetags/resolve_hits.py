from library.models import Source
from django import template

register = template.Library()

@register.simple_tag
def resolve_hits(**kwargs):
	'''Resolve number of hits from ordered list of sources'''
	field = kwargs['source_field']
	letter = kwargs['first_letter']
	return Source.objects.field_sort(letter, field).count()
