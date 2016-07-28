from django.contrib import admin
from library.models import LibraryItem, LibraryCollection
from library.models import LibraryPage, LibraryExcerpt
from gentext.models.bib import Author, Publisher


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('last_name', 'first_name')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


class LibraryCollectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('title',)
    fields = (
        'title',
        'collection_type',
        'collection',
        'info',
        'publication_period',
        'image',
        'slug'
        )


class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'item_type')
    search_fields = (
        'title',
        'item_type',
        'collection__title',
        'date',
        'author__last_name',
        'publisher__city',
        'publisher__name',
        )
    filter_horizontal = ('author',)


class LibraryPageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'item', 'image', 'slug')
    search_fields = ('item__title', 'page_number')
    fields = ('item', 'page_number', 'actual_pagenumber', 'image')
    raw_id_fields = ('item',)


class LibraryExcerptAdmin(admin.ModelAdmin):
    list_display = (
        'content',
        'item',
        'page',
        )
    search_fields = ('content', 'item__title')
    fields = (
        'content',
        'item',
        'page',
        'place',
        'x',
        'y',
        'w',
        'h',
        )

admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(LibraryItem, LibraryItemAdmin)
admin.site.register(LibraryCollection, LibraryCollectionAdmin)
admin.site.register(LibraryPage, LibraryPageAdmin)
admin.site.register(LibraryExcerpt, LibraryExcerptAdmin)
