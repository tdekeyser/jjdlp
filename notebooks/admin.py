from django.contrib import admin
from notebooks.models import NotebookCollection, Notebook, NotebookPage, Note


class NotebookCollectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = (
        'title',
        )
    fields = (
        'title',
        'collection',
        'info',
        )


class NotebookAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = (
        'name',
        'item_type',
        )
    fields = (
        'name',
        'collection',
        'text',
        'info',
        'item_type',
        'draft_period',
        'link',
        'libraryitem'
        )
    filter_horizontal = ('libraryitem',)


class NotebookPageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'image', 'slug')
    search_fields = ('page_number',)
    fields = ('notebook', 'page_number', 'image')


class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'page',
        'notejj',
        'annotation',
        'ctransfer',
        'msinfo',
        'source',
        'textref'
        )
    search_fields = ('notejj', 'page__page_number', 'source')
    fields = (
        'noteb',
        'page',
        'notejj',
        'annotation',
        'msinfo',
        'ctransfer',
        'source',
        'textline',
        'manuscriptexcerpt',
        'libraryexcerpt',
        'note'
        )
    filter_horizontal = ('libraryexcerpt',)
    raw_id_fields = ('page', 'textline', 'note')

admin.site.register(NotebookCollection, NotebookCollectionAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(NotebookPage, NotebookPageAdmin)
admin.site.register(Note, NoteAdmin)
