from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='splitondot')
@stringfilter
def splitondot(value):
	return value.split('.')[1]

@register.filter(name='splitoncomma')
@stringfilter
def splitoncomma(value):
	return value.split(',')[1]

@register.filter(name="novelpagesplitter")
@stringfilter
def novelpagesplitter(value):
	return value.split()[1].split('.')[0]

@register.filter(name='sanitize')
@stringfilter
def sanitize(value):
	return value.replace('.', '').lower()
