from django.db import models
from django.db.models import Q


# class CollectionQuerySet(models.query.QuerySet):
#     def get_frontcover(self):
#         return self.first.image


class PageQuerySet(models.query.QuerySet):
    '''Defines methods to easily get specific pages'''

    def get_frontcover(self):
        return self.get(page_number__contains='frontcover').image

    def get_backcover(self):
        return self.get(page_number__contains='backcover').image

    def get_singleimage(self, req_page):
        return self.get(page_number__contains=req_page).image

    def get_coverimages(self):
        # coverimages except frontcover
        coverimage_queryset = self.filter(
            Q(page_number__contains='title-page') |
            Q(page_number__contains='flyleaf') |
            Q(page_number__contains='half-title') |
            Q(page_number__contains='ex-libris') |
            Q(page_number__contains='note') |
            Q(page_number__contains='epigraph') |
            Q(page_number__contains='colophon') |
            Q(page_number__contains='table-of-contents') |
            Q(page_number__contains='chart') |
            Q(page_number__contains='acknowledgement') |
            Q(page_number__contains='frontispiece') |
            Q(page_number__contains='dedication') |
            Q(page_number__contains='bibliography') |
            Q(page_number__contains='index') |
            Q(page_number__contains='backcover')
        )
        return coverimage_queryset

    def get_detailimages(self):
        # all except coverimages
        contentimage_queryset = self.exclude(
            Q(page_number__contains='frontcover') |
            Q(page_number__contains='flyleaf') |
            Q(page_number__contains='title-page') |
            Q(page_number__contains='half-title') |
            Q(page_number__contains='ex-libris') |
            Q(page_number__contains='note') |
            Q(page_number__contains='epigraph') |
            Q(page_number__contains='colophon') |
            Q(page_number__contains='table-of-contents') |
            Q(page_number__contains='chart') |
            Q(page_number__contains='acknowledgement') |
            Q(page_number__contains='frontispiece') |
            Q(page_number__contains='dedication') |
            Q(page_number__contains='bibliography') |
            Q(page_number__contains='index') |
            Q(page_number__contains='backcover')
        )
        return contentimage_queryset

    def get_all_images_but_frontcover(self):
        contentimage_queryset = self.exclude(
            Q(page_number__contains='frontcover')
        )
        return contentimage_queryset

    def reorder(self, queryset):
        '''
        Sets reordering of queryset pages.
        Override it with custom ordering.
        '''
        return queryset

    def get_allsurroundingimages(self, req_page):
        '''
        Returns dictionary with a requested image and its neighbours
        '''
        chosen_image = self.get(page_number__exact=req_page)

        previous_images = []
        next_images = []
        chosen_index = None

        # get ordered queryset
        contentimages = self.reorder(self.get_all_images_but_frontcover())

        for index, item in enumerate(contentimages):
            if item == chosen_image:
                chosen_index = index
            else:
                if chosen_index is None:
                    previous_images.append(item)
                else:
                    next_images.append(item)

        get_images = {
            'chosen_image': chosen_image,
            'previous_images': previous_images,
            'next_images': next_images,
            }

        return get_images

    def get_two_surroundingimages(self, req_page):
        '''Returns previous and next image'''
        all_images = self.get_allsurroundingimages(req_page)

        get_images = {
                    'previous_image': all_images['previous_images'][-1] if all_images['previous_images'] else '',
                    'chosen_image': all_images['chosen_image'],
                    'next_image': all_images['next_images'][0] if all_images['next_images'] else ''
                }

        return get_images
