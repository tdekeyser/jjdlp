from django.contrib import admin
from notebooks.models import Notebook, NotebookPage, Note


class NotebookAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = (
        'name',
        'item_type',
        )
    fields = (
        'name',
        'info',
        'item_type',
        'draft_period',
        'link',
        'libraryitem'
        )
    filter_horizontal = ('libraryitem',)


class NotebookPageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'image')
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
        'novelline'
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
        'novelline',
        'manuscriptexcerpt',
        'libraryexcerpt'
        )
    filter_horizontal = ('libraryexcerpt',)
    raw_id_fields = ('page', 'novelline',)

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(NotebookPage, NotebookPageAdmin)
admin.site.register(Note, NoteAdmin)
