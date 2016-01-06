from django.contrib import admin
from notebooks.models import Notebook, NotebookPage, Note

class NotebookPageInline(admin.TabularInline):
    model = NotebookPage

class NoteInline(admin.TabularInline):
	model = Note

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
	inlines = [
        NotebookPageInline,
    ]

class NotebookPageAdmin(admin.ModelAdmin):
	list_display = ('page_number', 'image')
	search_fields = ('page_number',)
	fields = ('notebook', 'page_number', 'image')
	inlines = [
		NoteInline,
	]

class NoteAdmin(admin.ModelAdmin):
	list_display = (
		'notepage',
		'notejj',
		'annotation',
		'ctransfer',
		'msinfo',
		'source_info',
		'novelline'
		)
	search_fields = ('notejj',)
	fields = (
		'noteb',
		'notepage',
		'notejj',
		'annotation',
		'msinfo',
		'ctransfer',
		'source_info',
		'novelline',
		'manuscriptexcerpt',
		'sourcepageexcerpt'
		)
	filter_horizontal = ('sourcepageexcerpt',)
	raw_id_fields = ('notepage', 'novelline',)

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(NotebookPage, NotebookPageAdmin)
admin.site.register(Note, NoteAdmin)
