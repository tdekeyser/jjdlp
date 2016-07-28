from django.contrib import admin
from texts.models import Novel, BookSection, Chapter, Page, Line

class NovelAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)

class BookSectionAdmin(admin.ModelAdmin):
	list_display = ('novel', '__unicode__')

class ChapterAdmin(admin.ModelAdmin):
	list_display = ('novel', 'booksection', '__unicode__',)

class PageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)

class LineAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', )

	search_fields = (
		'content',
		'linenumber',
		)

admin.site.register(Novel, NovelAdmin)
admin.site.register(BookSection, BookSectionAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Line, LineAdmin)

