from django.views.generic import ListView, DetailView


class BaseView(object):
    '''
    Generic base view;
    Defines very basic variables and methods
    '''
    pageQ = None
    item = None

    template = ''
    dummybase_template = ''

    def get_item(self):
        pass

    def pages(self):
        return self.pageQ

    def set_page_caller(self):
        pass

    def get_template_names(self, **kwargs):
        # override
        return self.template

    def get_context_data(self, **kwargs):
        # override
        context = super(BaseView, self).get_context_data(**kwargs)
        context['item'] = self.item
        context['dummy_base'] = self.dummybase_template
        return context


class BaseListView(BaseView, ListView):
    pass


class BaseDetailView(BaseView, DetailView):
    pass
