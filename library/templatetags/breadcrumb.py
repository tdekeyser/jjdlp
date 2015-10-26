from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.simple_tag
def breadcrumb(**kwargs):
	'''
	Create breadcrumb
	Variable paths is composed of split_url, containing all absolute paths, 
	i.e. if split_url = ['library', 'fast-search'], then paths = ['library', 'library/fast-search']
	'''
	def form_absolute_paths(url_list):
		paths = []

		for url in url_list:
			path = []
			i = url_list.index(url) 
			while i > 0:
				# creates the desired list, but reversed
				path.append(url_list[i])
				i -= 1
			
			paths.append('/'.join(p for p in path[::-1])) # path[::-1] is the reversed list of path

		return paths

	split_url = kwargs['url'].split('/')
	absolutes = form_absolute_paths(split_url)

	u = '''
			<li>
				<a href="/">home</a>
			</li>
		'''

	for index in range(len(split_url)-2):
		if len(split_url[index]):
			u += '<li><a href="/{0}">{1}</a></li>'.format(absolutes[index], split_url[index])

	u += '<li class="active">{}</li>'.format(split_url[-2]) # add second last element (last is always empty) as active

	return u
