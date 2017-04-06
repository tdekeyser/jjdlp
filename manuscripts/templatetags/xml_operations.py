from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup
import re

register = template.Library()


@stringfilter
@register.simple_tag
def show_ref_tag(xml):
    '''
    Tag that takes as input XML and inserts links at each <ref> tag
    '''
    soup = BeautifulSoup(xml, 'html.parser')

    # first create list of links that should be inserted
    linklist = []
    for ref in soup.find_all('ref'): # find all references under 'corresp' attribute
        if ref.get('corresp'):
            c = remove_starting_zero(ref.get('corresp').replace('#', ''))
            n = remove_starting_zero(c[:-4])
            link = '<a class="ref" n="'+n+'" href="/notebooks/finnegans-wake-notebooks/VI.'+n+'./VI.'+c+'">[' + c + ']</a>'  # c in form '#xxxxx'
            linklist.append(link)
        else:
            linklist.append('')

    # then insert each link step by step
    newxml = ''
    i = 0                       # iterating index
    k = 0                       # last index copied of xml
    for f in re.compile('<ref').finditer(xml):
        start = f.start()
        newxml += xml[k:start] + linklist[i]
        k = start
        i += 1
    newxml += xml[k:]           # need to add the rest of the xml after last <ref> tag

    return newxml


def remove_starting_zero(x):
    '''
    Some notebooks have 'B.06', whereas the database does not include the
    starting 0s. This function removes them, returning e.g. 'B.6'.
    '''
    s = x.split('.')
    s[1] = str(int(s[1]))
    return '.'.join(st for st in s)
