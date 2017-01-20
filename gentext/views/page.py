from django.core.exceptions import ObjectDoesNotExist

from gentext.views.base import BaseDetailView


class PageView(BaseDetailView):
    itemslug = ''
    pageslug = ''

    page = None
    parent_model = None

    def get_item(self):
        '''
        Overridable;
        Finds parent item.
        '''
        return self.parent_model.objects.get(slug=self.kwargs[self.itemslug])

    def set_page_caller(self):
        '''
        Overridable;
        Set caller to query manager.
        '''
        self.pageQ = self.get_item().page_set

    def get_page(self):
        '''
        Overridable;
        Finds page = main request.
        '''
        return self.pageQ.get(slug=self.kwargs[self.pageslug])

    def get_pagenumber(self):
        return self.page.page_number

    def get_frontcover(self):
        try:
            return self.pageQ.get_frontcover()
        except ObjectDoesNotExist:
            return self.pageQ.none()

    def _get_surrounding_pages(self):
        '''
        Returns previous and next page of main request.
        '''
        return self.pageQ.get_two_surroundingimages(self.get_pagenumber())

    def get_object(self, **kwargs):
        # override
        self.item = self.get_item()
        # set page caller to find correct page
        self.set_page_caller()
        self.page = self.get_page()
        return self.page

    def get_context_data(self, **kwargs):
        # override
        context = super(PageView, self).get_context_data(**kwargs)
        # find surrounding images
        surroundings = self._get_surrounding_pages()
        # setup context
        context['item'] = self.item
        context['frontcover'] = self.get_frontcover()
        context['current_page'] = surroundings['current_page']
        context['previous_page'] = surroundings['previous_page']
        context['next_page'] = surroundings['next_page']
        return context
