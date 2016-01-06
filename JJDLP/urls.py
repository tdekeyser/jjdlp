from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, RedirectView
from library.models import Source

import re

# Base urls
from JJDLP import views
# static solely for developement:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='JJDLP/JJDLP_base.html'), name='home'),
	url(r'^about/$', TemplateView.as_view(template_name='JJDLP/JJDLP_about.html'), name='about'),
	url(r'^bibliography/$', TemplateView.as_view(template_name='JJDLP/JJDLP_bibliography.html'), name='bibliography'),
	url(r'^stats/$', views.StatsView.as_view(), name='stats'),
	url(r'^docs/$', views.DocsView.as_view(), name='docs'),
	url(r'^favicon\.ico$', RedirectView.as_view(url='static/JJDLP/images/favicon.ico', permanent=True)),
	url(r'^advanced-search/', views.AdvancedSearchView(), name='haystack_search'),
	url(r'^search-docs/$', TemplateView.as_view(template_name='search/search_docs.html'), name='search_docs'),
)

# library urls
from library import views, forms

urlpatterns += patterns('',
	url(r'^library/$', views.LibraryHomeView.as_view(), name='library_home'),
	url(r'^library/fast-search/', views.LibrarySearchView(), name='library_fast_search'),
	url(r'^library/(?P<source_field>\w+)/$', RedirectView.as_view(url='A', permanent=True)),
	url(r'^library/(?P<source_field>\w+)/(?P<first_letter>[A-Z])/$', views.SourceListLetter.as_view(), name='order_all'),
	url(r'^library/item:(?P<slug>[-_\w]+)/$', views.SourceDetail.as_view(), name='source_detail'),
	url(r'^library/collection:(?P<slug>[-_\w]+)/$', views.CollectionDetail.as_view(), name='sourcecollection_detail'),
	url(r'^library/item:(?P<itemslug>[-_\w]+)/(?P<req_page>[^/]+)/$', views.SourcePageDetail.as_view(), name='librarypage_detail'),
	# url(r'^library/certainty-of-use-regulation$', TemplateView.as_view(template_name='library/certainty_regulation.html'), name='cou_regulations'),
)

# notebooks urls
from notebooks import views
urlpatterns += patterns('',
	url(r'^notebooks/$', views.NotebookHomeView.as_view(), name='notebooks_home'),
	url(r'^notebooks/fast-search/', views.NoteSearchView(), name='notebooks_fast_search'),
	url(r'^notebooks/(?P<noteb>[A-Z][.]\d+)/$', views.NotebookView.as_view(), name='notebook_detail'),
	url(r'^notebooks/(?P<noteb>[A-Z][.]\d+)/(?P<notebpage>[A-Z][.]\d+[.][^/]+)/$', views.NotebookPageDetail.as_view(), name='notebookpage_detail'),
	)
#\d+[-]?\d+?

# manuscripts urls
from manuscripts import views
urlpatterns += patterns('',
	url(r'^manuscripts/$', views.ManuscriptsHomeView.as_view(), name='manuscripts_home'),
	url(r'^manuscripts/fast-search/', views.ManuscriptsSearchView(), name='manuscripts_fast_search'),
	url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/$', views.ManuscriptCollectionView.as_view(template_name='manuscripts/manuscripts_detail.html', paginate_by=8), name='manuscripts_detail'),
	url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/enlist/$', views.ManuscriptCollectionView.as_view(template_name='manuscripts/manuscripts_pagelist.html', paginate_by=10), name='manuscripts_pagelist'),
	url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/(?P<manuscriptpage>[-_\w]+)/$', views.ManuscriptPageView.as_view(), name='manuscriptpage_detail'),
	)

# novels urls
from novels import views
urlpatterns += patterns('',
	url(r'^novels/$', views.NovelsHomeView.as_view(), name='novels_home'),
	url(r'^novels/fast-search/', views.NovelsSearchView(), name='novels_fast_search'),
	url(r'^novels/(?P<novelslug>[-_\w]+)/$', views.NovelDetailView.as_view(), name='novel_detail'),
	url(r'^novels/(?P<novelslug>[-_\w]+)/(?P<novelpage>\d+)/$', views.NovelPageView.as_view(), name='novelpage_detail'),	
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
