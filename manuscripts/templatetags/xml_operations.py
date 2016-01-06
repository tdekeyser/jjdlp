from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup
import re

register = template.Library()

@stringfilter
@register.simple_tag
def show_ref_tag(xml):
	'''Tag that takes as input XML and inserts links at each <ref> tag'''
	soup = BeautifulSoup(xml, 'lxml')
	
	# first create list of links that should be inserted
	linklist = []
	for ref in soup.find_all('ref'): # find all references under 'corresp' attribute
		if ref.get('corresp'):
			c = ref.get('corresp').replace('#', '')
			n = c[:-4]
			link = '<a class="ref" n="'+n+'" href="/notebooks/'+n+'/'+c+'">[' + c + ']</a>'  # c in form '#xxxxx'
			linklist.append(link)
		else:
			linklist.append('')

	# then insert each link step by step
	newxml = ''
	i = 0						# iterating index
	k = 0						# last index copied of xml
	for f in re.compile('<ref').finditer(xml):
		start = f.start()
		newxml += xml[k:start] + linklist[i]
		k = start
		i += 1
	newxml += xml[k:]			# need to add the rest of the xml after last <ref> tag

	return newxml
