from django.db import models

from generic.managers.queryset import PageQuerySet


class SourceQuerySet(models.query.QuerySet):
    '''Manager that generates customised querysets for sources'''
    def get_frontcover(self):
        pass

    def get_coverimages(self):
        pass

    def get_detailimages(self):
        pass


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


class NotebookPageQuerySet(PageQuerySet):
    '''Notebook-specific queryset manager'''

    def get_traced_objects_list(self, nbpageobject):
        '''Returns all sources and novelpages on one novelpage'''
        traced_sources = []
        traced_manuscripts = []
        traced_novellines = []

        for note in nbpageobject.note_set.all():

            # first check traced sourceexcerpt
            if note.libraryexcerpt:
                for libraryexcerpt in note.libraryexcerpt.all():
                    if libraryexcerpt not in traced_sources:
                        traced_sources.append(libraryexcerpt.item)

            # check manuscripts
            if note.manuscriptexcerpt and note.manuscriptexcerpt.manuscriptpage not in traced_manuscripts:
                traced_manuscripts.append(note.manuscriptexcerpt.manuscriptpage)

            # then check novellines
            if note.novelline and note.novelline not in traced_novellines:
                traced_novellines.append(note.novelline)

        traced_objects = {
                    'traced_sources': traced_sources,
                    'traced_sources_count': len(traced_sources),
                    'traced_manuscripts': traced_manuscripts,
                    'traced_manuscripts_count': len(traced_manuscripts),
                    'traced_novellines': traced_novellines,
                    'traced_novellines_count': len(traced_novellines)
                }

        return traced_objects


class ManuscriptPageQueryset(PageQuerySet):

    def get_two_surroundingimages(self, req_page):
        '''
        @override
        Manuscript pages have been ordered by numerical_order field.
        '''
        try:
            previous_image = self.filter(numerical_order__lt=req_page).reverse()[0]
        except IndexError:
            previous_image = ''

        try:
            next_image = self.filter(numerical_order__gt=req_page)[0]
        except IndexError:
            next_image = ''

        get_images = {
                    'previous_image': previous_image,
                    'next_image': next_image,
                    'chosen_image': None
                }

        return get_images
