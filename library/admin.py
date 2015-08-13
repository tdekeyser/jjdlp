from django.contrib import admin
from library.models import Source, Author, Publisher, Usage, SourcePage

class SourceAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'get_usage')
	search_fields = (
		'source_type',
		'title',
		'publication_date',
		'author__last_name',
		'publisher__city',
		'publisher__publisher_name',
		'usage__used_book',
		'usage__used_book_chapter',
		'lib_type',
		)
	filter_horizontal = ('author', 'usage')

	def get_usage(self, obj):
		return "\n&\n".join([u'%s %s' % (u.used_book, u.used_book_chapter) for u in obj.usage.all()])

class SourcePageAdmin(admin.ModelAdmin):
	list_display = ('source_ref', 'page_number', 'image')
	search_fields = ('source_ref__title',)
	fields = ('source_ref', 'page_number', 'image')
	raw_id_fields = ('source_ref',)

# class SourcePageInline(admin.TabularInline):
#     model = SourcePage

# class SourceAdmin(admin.ModelAdmin):
#     inlines = [
#         SourcePageInline,
#     ]

admin.site.register(Source, SourceAdmin)
admin.site.register(SourcePage, SourcePageAdmin)
