# Defines custom queryset managers

from django.db import models
from django.db.models import Q

class SourceQuerySet(models.query.QuerySet):
	'''Manager that generates customised querysets for sources'''
	def field_sort(self, letter, source_field):
		if source_field == 'author':
			return self.filter(author__last_name__startswith=letter).order_by('author__last_name')
		if source_field == 'title':
			return self.filter(title__startswith=letter).order_by('title')
		if source_field == 'city':
			return self.filter(publisher__city__startswith=letter).order_by('publisher__city')

class PageQuerySet(models.query.QuerySet):
	'''Manager that generates customised querysets for getting pages'''

	def get_frontcover(self):
		return self.get(page_number__contains='frontcover').image

	def get_backcover(self):
		return self.get(page_number__contains='backcover').image

	def get_singleimage(self, req_page):
		'''Get requested image'''
		return self.get(page_number__contains=req_page).image

	def get_coverimages(self):
		'''Returns queryset of cover images'''
		pass

	def get_detailimages(self):
		'''Returns queryset of images excluding coverimages'''
		pass

	def get_all_images_but_frontcover(self):
		'''Returns queryset of images excluding frontcover'''
		contentimage_queryset = self.exclude(
			Q(page_number__contains='frontcover')
		)
		return contentimage_queryset

	def get_allsurroundingimages(self, req_page, needReordering=False):
		'''
		Returns dictionary with a requested image objects and its neighbours

		!!! Includes the library-specific function order_by_actualpagenumber(); delete if not needed !!!

		'''
		chosen_image = self.get(page_number__contains=req_page)

		previous_images = []
		next_images = []
		chosen_index = None

		if needReordering:
			contentimages = self.order_by_actualpagenumber(self.get_all_images_but_frontcover())
		else:
			contentimages = self.get_all_images_but_frontcover()

		for index, item in enumerate(contentimages):
			if item == chosen_image:
				chosen_index = index
			else:
				if chosen_index == None:
					previous_images.append(item)
				else:
					next_images.append(item)

		get_images = {
			'chosen_image': chosen_image,
			'previous_images': previous_images,
			'next_images': next_images,
			}

		return get_images

	def get_two_surroundingimages(self, req_page, needReordering=False):
		'''
		Returns dictionary with 2 objects: previous and next image
		'''
		all_images = self.get_allsurroundingimages(req_page, needReordering)

		get_images = {
					'previous_image': all_images['previous_images'][-1] if all_images['previous_images'] else '',
					'chosen_image': all_images['chosen_image'],
					'next_image': all_images['next_images'][0] if all_images['next_images'] else ''
				}

		return get_images

class LibraryPageQuerySet(PageQuerySet):
	# library-specific queryset manager; inherits everything from PageQuerySet

	def get_coverimages(self): # coverimages except frontcover
		coverimage_queryset = self.filter(
			Q(page_number__contains='title-page') |
			Q(page_number__contains='half-title') |
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

	def get_detailimages(self): # all except coverimages
		contentimage_queryset = self.exclude(
			Q(page_number__contains='frontcover') |
			Q(page_number__contains='title-page') |
			Q(page_number__contains='half-title') |
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

	def order_by_actualpagenumber(self, queryset):
		'''
		As a SourcePage object's actual_pagenumber cannot be an IntegerField (some pages may include hyphens),
		a library-specific queryset ordering on actual_pagenumber is needed.
		This function forces a numerical order of a given queryset.
		'''

		return queryset.extra(
							select={'library_sourcepage_actual_pagenumber': "CONVERT(SUBSTRING_INDEX(actual_pagenumber,'-',1),UNSIGNED INTEGER)"}
							).order_by('library_sourcepage_actual_pagenumber')

class NotebookPageQuerySet(PageQuerySet):
	# notebook-specific queryset manager

	def get_coverimages(self): # only coverimages, but not frontcover
		coverimage_queryset = self.filter(
			Q(page_number__contains='backcover')
		)
		return coverimage_queryset

	def get_detailimages(self): # all but coverimages
		contentimage_queryset = self.exclude(
			Q(page_number__contains='frontcover') |
			Q(page_number__contains='backcover')
		)
		return contentimage_queryset

	def get_traced_objects_list(self, nbpageobject):
		'''Returns all sources and novelpages on one novelpage'''
		traced_sources = []
		traced_manuscripts = []
		traced_novellines = []

		for note in nbpageobject.note_of_page.all():

			# first check traced sourceexcerpt
			if note.sourcepageexcerpt:
				for sourceexcerpt in note.sourcepageexcerpt.all():
					# if the excerpt not already in traced_sources, then add it to the list
					if sourceexcerpt not in traced_sources:
						traced_sources.append(sourceexcerpt.source)

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
