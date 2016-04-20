from django import template
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from library.models import LibraryItem, LibraryPage
from library.models import LibraryCollection

register = template.Library()


def slugify_object_repr(text):
    return slugify(str(text).split()[:4])


@register.simple_tag
def get_action_url(**kwargs):
    '''
    Find the page urls of the recent_actions
    '''
    action = kwargs['action']

    if 'page' in str(action.content_type):
        page = LibraryPage.objects.get(page_number=action.object_repr)
        parent = page.item
        return reverse('library_page', kwargs={'itemslug': parent.slug, 'req_page': page.actual_pagenumber})
    else:
        slug = slugify_object_repr(action.object_repr)
        if 'collection' in str(action.content_type):
            col = LibraryCollection.objects.get(slug__icontains=slug)
            return reverse('library_collection', kwargs={'slug': col.slug})
        elif 'item' in str(action.content_type):
            it = LibraryItem.objects.get(slug__icontains=slug)
            return reverse('library_item', kwargs={'slug': it.slug})
        else:
            return ''
