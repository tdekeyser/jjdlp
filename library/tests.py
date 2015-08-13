# do python manage.py test library

from django.test import TestCase
from library.models import Author, Usage, Source, SourcePage

def create_source(title, pub_date):
	'''Create new source with minimum information'''
	return Source(title=title, publication_date=pub_date)

def create_page(source_ref, page_number):
	'''Create page'''
	return SourcePage(source_ref=source_ref,page_number=page_number)


class SourceModelTests(TestCase):	
	def test_if_new_source_creates_proper_slug(self):
		'''Checks whether a proper slug has been created on save()'''
		new_source = create_source('Example Title of a New Source With a Long Title', 2015)
		new_source.save()
		self.assertEqual('example-title-of-a-new-source-with', new_source.slug)

	def test_if_new_source_generates_getauthors_and_getusage(self):
		'''Check get_authors() and get_usage()'''
		author1 = Author(last_name='Joyce', first_name='James')
		author1.save()
		author2 = Author(last_name='Barnacle', first_name='Nora')
		author2.save()

		usage1 = Usage(used_book='Finnegans Wake', used_book_chapter="III.3")
		usage1.save()
		usage2 = Usage(used_book='Ulysses', used_book_chapter="18")
		usage2.save()

		new_source = create_source('Example Title of a New Source With a Long Title', 2015)
		new_source.save()

		new_source.author.add(author1, author2)
		new_source.usage.add(usage1, usage2)

		self.assertEqual('Nora Barnacle & James Joyce', new_source.get_authors())
		self.assertEqual('Finnegans Wake III.3 & Ulysses 18', new_source.get_usage())

class SourceDetailTests(TestCase):
	def test_order_of_get_contentimages(self):
		'''Contentimages converts alphabetically ordered queryset to a numerical order'''
		source = create_source('Example Title', 2015)
		source.save()

		page1 = create_page(source, 'TES-TES,2-3')
		page1.save()
		page2 = create_page(source, 'TES-TES,44-45')
		page2.save()
		page3 = create_page(source, 'TES-TES,106-107')
		page3.save()

		self.assertEqual([page1,page2,page3], list(source.page_source.order_by_actualpagenumber(source.page_source.get_contentimages())))

	def test_order_of_surroundingimages(self):
		'''Surroundingimages should create a list of previous and next images, excluding the actual image'''
		source = create_source('Example Title', 2015)
		source.save()

		page1 = create_page(source, 'TES-TES,2-3')
		page1.save()
		page2 = create_page(source, 'TES-TES,44-45')
		page2.save()
		page3 = create_page(source, 'TES-TES,106-107')
		page3.save()

		self.assertEqual([], source.page_source.get_allsurroundingimages('2-3')['previous_images'])
		self.assertEqual([page2,page3], source.page_source.get_allsurroundingimages('2-3')['next_images'])
		self.assertEqual([page1], source.page_source.get_allsurroundingimages('44-45')['previous_images'])
		self.assertEqual([page3], source.page_source.get_allsurroundingimages('44-45')['next_images'])
		self.assertEqual([page1,page2], source.page_source.get_allsurroundingimages('106-107')['previous_images'])
		self.assertEqual([], source.page_source.get_allsurroundingimages('106-107')['next_images'])
