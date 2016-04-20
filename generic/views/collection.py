from django.core.exceptions import ObjectDoesNotExist

from generic.views.item import ItemView


class CollectionView(ItemView):

    def set_page_caller(self):
        # override
        self.pageQ = self.get_item().item_set

    def _compile_pages(self):
        # override
        try:
            self.frontcover = self.item.image
        except ObjectDoesNotExist:
            self.frontcover = self.pageQ.none()
        self.covers = self.pageQ.none()
        self.details = self.pageQ.all()

    def get_context_data(self, **kwargs):
        # override
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['data_type'] = 'Collection'
        context['list_type'] = 'Items'
        return context
