from django.contrib import admin
from manuscripts.models import Manuscript, ManuscriptPage, ManuscriptExcerpt


class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('title',)
    fields = (
        'title',
        'frontcover',
        'info',
        'note_on_transcriptions',
        'text',
        'slug',
        )


class ManuscriptPageAdmin(admin.ModelAdmin):
    list_display = (
        'page_number',
        'numerical_order',
        'image',
        'transcription',
        'info'
        )
    search_fields = ('page_number', 'transcription',)
    fields = (
        'manuscript',
        'page_number',
        'numerical_order',
        'image',
        'transcription',
        'info'
        )


class ManuscriptExcerptAdmin(admin.ModelAdmin):
    list_display = (
        'manuscript',
        'content',
        'manuscriptpage',
        )
    search_fields = ('content',)
    fields = (
        'manuscript',
        'content',
        'manuscriptpage'
        )


admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(ManuscriptPage, ManuscriptPageAdmin)
admin.site.register(ManuscriptExcerpt, ManuscriptExcerptAdmin)
