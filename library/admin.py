from django.contrib import admin
from library.models import Source, SourceCollection, Author, Publisher, SourcePage, SourceExcerpt

class SourcePageInline(admin.TabularInline):
    model = SourcePage

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)

class PublisherAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)

class SourceCollectionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)
	search_fields = ('title',)
	fields = (
		'title',
		'collection_type',
		'info',
		'publication_period',
		'image',
		)

class SourceAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)
	search_fields = (
		'source_type',
		'collection__title',
		'title',
		'publication_date',
		'author__last_name',
		'publisher__city',
		'publisher__publisher_name',
		'lib_type',
		)
	filter_horizontal = ('author', 'usage')
	inlines = [
		SourcePageInline,
		]

class SourcePageAdmin(admin.ModelAdmin):
	list_display = ('page_number', 'source', 'image')
	search_fields = ('source__title',)
	fields = ('source', 'page_number', 'actual_pagenumber', 'image')
	raw_id_fields = ('source',)

class SourceExcerptAdmin(admin.ModelAdmin):
	list_display = (
		'content',
		'source',
		'sourcepage',
		)
	search_fields = ('content',)
	fields = (
		'content',
		'source',
		'sourcepage',
		'place',
		'x',
		'y',
		'w',
		'h',
		)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(SourceCollection, SourceCollectionAdmin)
admin.site.register(SourcePage, SourcePageAdmin)
admin.site.register(SourceExcerpt, SourceExcerptAdmin)
