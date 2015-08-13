from django import template
from pattern.vector import Document, distance, NB
from pattern.db import csv
import re

register = template.Library()

@register.simple_tag
def resolve_certainty(certainty_info):
	'''Resolve certainty with Naive Bayes'''
	if certainty_info == '':
		return 'No certainty info.'
	else:
		nb = NB()
		for observation, certainty in csv('library/templatetags/c_training_data.csv'):
			v = Document(observation, type=int(certainty), stopwords=True)
			nb.train(v)
		return nb.classify(Document(certainty_info))

	# mark_safe(re.sub(r'<div class="square" style="border:15px solid black; width:10px"/>'))

@register.simple_tag
def resolve_colour(certainty_info):
	'''Resolve colour based on resolve_certainty()'''
	if resolve_certainty(certainty_info)==1:
		return "#FF0000"
	elif resolve_certainty(certainty_info)==2:
		return "#FFBF00"
	elif resolve_certainty(certainty_info)==3:
		return "#FFFF00"
	elif resolve_certainty(certainty_info)==4:
		return "#40FF00"

