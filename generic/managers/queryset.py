from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.core.paginator import Paginator


class PageQuerySet(models.query.QuerySet):
    '''Defines methods to easily get specific pages'''

    def get_frontcover(self):
        try:
            return self.get(page_number__contains='frontcover')
        except ObjectDoesNotExist:
            return self.all().first()

    def get_backcover(self):
        return self.get(page_number__contains='backcover')

    def get_singleimage(self, req_page):
        return self.get(page_number__contains=req_page)

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

    def all_but_frontcover(self):
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
        contentimages = self.reorder(self.all_but_frontcover())

        for index, item in enumerate(contentimages):
            if item == chosen_image:
                chosen_index = index
            else:
                if chosen_index is None:
                    previous_images.append(item)
                else:
                    next_images.append(item)

        get_images = {
            'current_image': chosen_image,
            'previous_images': previous_images,
            'next_images': next_images,
            }

        return get_images

    def get_two_surroundingimages(self, req_page):
        '''Returns previous and next image'''
        images = self.reorder(self.all_but_frontcover())
        # create paginator to find next and previous images
        p = Paginator(images, 1)

        # get index in ordered queryset
        current_index = 0
        current_image = self.get(page_number__exact=req_page)
        for index, item in enumerate(images):
            if item == current_image:
                current_index = index + 1
                break

        # get next and previous image
        current_page = p.page(current_index)
        next_image = None
        previous_image = None
        if current_page.has_next():
            next_image = p.page(current_index+1).object_list[0]
        if current_page.has_previous():
            previous_image = p.page(current_index-1).object_list[0]

        return {
            'previous_image': previous_image,
            'current_image': current_image,
            'next_image': next_image
        }
