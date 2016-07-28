from generic.views.item import ItemView


class CollectionView(ItemView):

    def get_item(self):
        # override
        c = self.kwargs[self.slug_name].split('/')[-1]
        return self.model.objects.get(slug=c)

    def set_page_caller(self):
        # override
        self.pageQ = self.get_item().item_set

    def _compile_pages(self):
        # override
        self.frontcover = self.item
        self.covers = self.pageQ.none()
        self.details = self.pageQ.all()

    def get_context_data(self, **kwargs):
        # override
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['data_type'] = 'Collection'
        context['child_collections'] = self.get_item().collection_set.all()
        return context
