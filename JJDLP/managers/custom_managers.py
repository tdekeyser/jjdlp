from gentext.managers.queryset import PageQuerySet


class LibraryPageQuerySet(PageQuerySet):
    '''Library-specific queryset manager'''

    def reorder(self, queryset):
        '''
        @override
        Sets reordering of library pages.
        '''
        return self.order_by_actualpagenumber(queryset)

    def order_by_actualpagenumber(self, queryset):
        '''
        As a LibraryPage object's actual_pagenumber cannot be an IntegerField (some pages may include hyphens),
        a library-specific queryset ordering on actual_pagenumber is needed.
        This function forces a numerical order of a given queryset.
        '''
        return queryset.extra(
            select={'library_librarypage_actual_pagenumber': "CONVERT(SUBSTRING_INDEX(actual_pagenumber,'-',1),UNSIGNED INTEGER)"}
            ).order_by('library_librarypage_actual_pagenumber')


# class ManuscriptPageQueryset(PageQuerySet):

#     def get_two_surroundingimages(self, req_page):
#         '''
#         @override
#         Manuscript pages have been ordered by numerical_order field.
#         '''
#         try:
#             previous_image = self.filter(numerical_order__lt=req_page).reverse()[0]
#         except IndexError:
#             previous_image = ''

#         try:
#             next_image = self.filter(numerical_order__gt=req_page)[0]
#         except IndexError:
#             next_image = ''

#         get_images = {
#                     'previous_image': previous_image,
#                     'next_image': next_image,
#                     'chosen_image': None
#                 }

#         return get_images
