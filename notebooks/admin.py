from django.contrib import admin
from notebooks.models import *

class NotebookAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)
	search_fields = (
		'name',
		'info',
		'further_usage',
		'used_source__verbose_source_name',
		)
	raw_id_fields = ('used_source',)
	fields = ('name', 'info', 'further_usage')

class NotebookPageAdmin(admin.ModelAdmin):
	list_display = ('notebook_ref', 'page_number', 'image')
	search_fields = ('notebook_ref__title',)
	fields = ('notebook_ref', 'page_number', 'image')

class NoteAdmin(admin.ModelAdmin):
	list_display = ('notepage', 'notejj', 'source', 'source_info', 'annotation', 'msinfo', 'ctransfer')
	search_fields = ('notejj',)
	fields = ('notepage', 'notejj', 'source', 'source_info', 'annotation', 'msinfo', 'ctransfer')

class NotebookPageInline(admin.TabularInline):
    model = NotebookPage

class NoteInline(admin.TabularInline):
	model = Note

class NotebookAdmin(admin.ModelAdmin):
    inlines = [
        NotebookPageInline,
    ]

class NotebookPageAdmin(admin.ModelAdmin):
	inlines = [
		NoteInline,
	]


admin.site.register(Notebook, NotebookAdmin)
admin.site.register(NotebookPage, NotebookPageAdmin)
admin.site.register(Note, NoteAdmin)
