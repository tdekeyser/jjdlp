from django import template

register = template.Library()

@register.filter
def divide(value, arg):
	return int(value)/int(arg)

@register.filter
def absSubtract(value, arg):
	return abs(int(value)-int(arg))
	