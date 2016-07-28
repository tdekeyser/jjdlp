from gentext.views.base import BaseListView
from django.core.exceptions import ObjectDoesNotExist


class ItemView(BaseListView):
    '''
    Generic collection view
    Set model and slug name to get the main object.
    '''
    context_object_name = 'collection_list'
    model = None
    slug_name = ''

    frontcover = None
    covers = None
    details = None

    def get_item(self):
        '''
        Overridable;
        Get main object.
        '''
        return self.model.objects.get(slug=self.kwargs[self.slug_name])

    def set_page_caller(self):
        '''
        Overridable;
        Set caller to query manager.
        '''
        self.pageQ = self.get_item().page_set

    def _set_pages(self):
        '''
        Raise error if pageQ is none.
        '''
        if self.pageQ is not None:
            self._compile_pages()
        else:
            raise ObjectDoesNotExist

    def _compile_pages(self):
        '''
        Collect pages to be taken to queryset.
        '''
        self.frontcover = self.pageQ.get_frontcover()
        try:
            self.covers = self.pageQ.get_coverimages()
        except ObjectDoesNotExist:
            self.cover = self.pageQ.none()
        try:
            self.details = self.pageQ.get_detailimages()
        except ObjectDoesNotExist:
            self.details = self.pageQ.none()

    def _allocate_objects(self):
        '''
        Sets the requested object and pages
        '''
        self.item = self.get_item()
        self.set_page_caller()
        try:
            self._set_pages()
        except ObjectDoesNotExist:
            pass

    def get_queryset(self, **kwargs):
        '''
        @override
        Template name is context_object_name.

        Warning: Do not simply override without
        taking over queryset with super().
        '''
        # update objects
        self._allocate_objects()
        # pass detailpages as queryset
        if self.details is not None:
            return self.details
        else:
            return self.pageQ.none()

    def get_context_data(self, **kwargs):
        '''
        @override
        Sets some basic context.
        '''
        context = super(ItemView, self).get_context_data(**kwargs)
        # set basic info in context
        context['data_type'] = 'Item'
        context['covers'] = self.covers
        context['frontcover'] = self.frontcover
        # counts
        queryset_count = self.get_queryset().count()
        try:
            context['item_count'] = self.pageQ.count()
            context['detail_count'] = queryset_count
        except AttributeError:
            # no covers/details
            context['item_count'] = 0
            context['detail_count'] = 0

        return context
