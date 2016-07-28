'''
Provides functions with respect to bibliographical references. More
specifically, these functions allow Django model instances to be
translated into a valid reference.

In order to use these functions properly, the instance MUST have
getter methods available for all the desired bibliographical
information.
'''

# define bibliographic styles according to item type
BIBSTYLE = 'Chicago'
BIBTYPE = {
    'Chicago': {
        '': ['title'],
        'book': ['author', 'date', 'title', 'publisher'],
        'article': ['author', 'date', 'title'],
        'poem': ['author', 'date', 'title', 'publisher'],
        'newspaper': ['collection', 'title']
    },
}


def pybib(instance):
    '''
    Returns bibliographical reference of the instance. The instance
    must have a global getter method!
    '''
    try:
        item_type = instance.get_item_type()
        content = BIBTYPE[BIBSTYLE][item_type]
        data = [bibstring(get_field(instance, c)) for c in content]
        return u'. '.join(validate(data)) + '.'
    except AttributeError:
        raise AttributeError('No global getter method found!')


def get_field(instance, request):
    '''
    Global instance getter for bibliographic references
    '''
    if request == 'author':
        return instance.get_author()
    elif request == 'title':
        return instance.get_title()
    elif request == 'date':
        return instance.get_date()
    elif request == 'item_type':
        return instance.get_item_type()
    elif request == 'publisher':
        return instance.get_publisher()
    elif request == 'collection':
        return instance.get_collection()


def bibstring(data):
    '''
    Keeps track of unknown data and replaces it with a
    valid string.
    '''
    if not data:
        return u'Unknown'
    else:
        return u'{}'.format(data)


def validate(data):
    '''
    More checks before building the reference
    '''
    print data
    if data[0] == 'Unknown':
        # remove unknown authors from ref
        data = data[1:]
        # date behind title
        data[0], data[1] = data[1], data[0]
    # remove empty elements
    return filter(None, data)
