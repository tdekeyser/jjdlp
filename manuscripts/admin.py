from django.contrib import admin
from manuscripts.models import ManuscriptCollection, ManuscriptPage, ManuscriptExcerpt

class ManuscriptPageInline(admin.TabularInline):
    model = ManuscriptPage

class ManuscriptExcerptInline(admin.TabularInline):
	model = ManuscriptExcerpt

class ManuscriptCollectionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)
	search_fields = (
		'title',
		'homepage_info',
		'info',
		'note_on_transcriptions',
		'further_usage',
		# 'source',
		)
	# filter_horizontal = ('source',)
	fields = (
		'title',
		'frontcover',
		'homepage_info',
		'info',
		'note_on_transcriptions',
		'further_usage',
		# 'source'
		)
	inlines = [
        ManuscriptPageInline,
    ]

class ManuscriptPageAdmin(admin.ModelAdmin):
	list_display = (
		'manuscript',
		'page_number',
		'image',
		'transcription',
		'specific_pageinfo'
		)
	search_fields = ('page_number', 'transcription',)
	fields = ('manuscript', 'page_number')
	inlines = [
		ManuscriptExcerptInline,
	]

class ManuscriptExcerptAdmin(admin.ModelAdmin):
	list_display = (
		'manuscript',
		'manuscriptpage',
		'content'
		)
	search_fields = ('manuscriptpage', 'content')
	fields = (
		'manuscript',
		'manuscriptpage',
		'content',
		)

admin.site.register(ManuscriptCollection, ManuscriptCollectionAdmin)
admin.site.register(ManuscriptPage, ManuscriptPageAdmin)
admin.site.register(ManuscriptExcerpt, ManuscriptExcerptAdmin)
