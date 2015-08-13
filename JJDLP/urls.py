from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from library.models import Source
from haystack.query import SearchQuerySet

# Base urls
from JJDLP import views
# static solely for developement:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='JJDLP/JJDLP_base.html'), name='home'),
	url(r'^about/$', TemplateView.as_view(template_name='JJDLP/JJDLP_about.html'), name='about'),
	url(r'^stats/$', TemplateView.as_view(template_name='JJDLP/JJDLP_stats.html'), name='stats'),
	url(r'^favicon\.ico$', RedirectView.as_view(url='static/JJDLP/images/favicon.ico')),
	url(r'^advanced-search/', views.AdvancedSearchView(), name='haystack_search'),
	url(r'^search-docs/$', TemplateView.as_view(template_name='search/search_docs.html'), name='search_docs'),
)

# library urls
from library import views, forms

urlpatterns += patterns('',
	url(r'^library/$', views.LibraryHomeView.as_view(), name='library_home'),
	url(r'^library/fast-search/$', views.FastSearchView(), name='library_fast_search'),
	url(r'^library/sorted/(?P<source_field>\w+)/(?P<first_letter>[A-Z])/$', views.SourceList_letter.as_view(), name='order_all'),
	url(r'^library/(?P<slug>[-_\w]+)/$', views.SourceDetail.as_view(), name='source_detail'),
	url(r'^library/(?P<slug>[-_\w]+)/(?P<req_page>[^/]+)/$', views.SourcePageDetail.as_view(), name='page_detail'),
	url(r'^library/certainty-of-use-regulation$', TemplateView.as_view(template_name='library/certainty_regulation.html'), name='cou_regulations'),
)

# notebooks urls
from notebooks import views
urlpatterns += patterns('',
	url(r'^notebooks/$', views.NotebookHomeView.as_view(), name='notebooks_home'),
	url(r'^notebooks/(?P<noteb>[A-Z][.]\d+)/$', views.NotebookView.as_view(), name='notebook_detail'),
	url(r'^notebooks/(?P<notebpage>[A-Z][.]\d+[.]\d+[-]?\d+?)/$', views.NotebookPageDetail.as_view(), name='notebookpage_detail'),
	)

# admin
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# static/media config if Debug=True
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
