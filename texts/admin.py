from django.contrib import admin
from texts.models import Text, Section, Chapter, Page, Line


class TextAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('text', '__unicode__')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('text', 'section', '__unicode__',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


class LineAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )

    search_fields = (
        'content',
        'linenumber',
        )


admin.site.register(Text, TextAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Line, LineAdmin)
