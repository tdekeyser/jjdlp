from django.conf.urls import patterns, url, include
from django.contrib import admin
# from django.views.decorators.cache import cache_page
# from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, RedirectView

from JJDLP.views import StatsView, DocsView, AdvancedSearchView
from JJDLP.views import ConnectView, ConnectTree, ConnectDatabase

from library.views import LibraryHomeView, LibraryMacroView, LibrarySearchView
from library.views import LibraryItemView, LibraryPageView
from library.views import LibraryCollectionView, LibraryExcerptView

from notebooks.views import NotebookHomeView, NoteSearchView
from notebooks.views import NotebookView, NotebookPageView

from manuscripts.views import ManuscriptsHomeView, ManuscriptsSearchView
from manuscripts.views import ManuscriptCollectionView, ManuscriptPageView

from novels.views import NovelsHomeView, NovelsSearchView
from novels.views import NovelDetailView, NovelPageView

# static solely for developement:
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='JJDLP/base.html'), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/JJDLP/images/favicon.ico', permanent=True)),
    url(r'^about/$', TemplateView.as_view(template_name='JJDLP/about.html'), name='about'),
    url(r'^bibliography/$', TemplateView.as_view(template_name='JJDLP/bibliography.html'), name='bibliography'),
    url(r'^stats/$', StatsView.as_view(), name='stats'),
    url(r'^docs/$', DocsView.as_view(), name='docs'),
    url(r'^docs/raw-markdown/$', DocsView.as_view(raw=True), name='docs_raw_markdown'),
    url(r'^advanced-search/', AdvancedSearchView(), name='haystack_search'),
    url(r'^search-docs/$', TemplateView.as_view(template_name='search/search_docs.html'), name='search_docs'),
    url(r'^connect/$', ConnectView.as_view(), name='connect'),
    url(r'^connect/get-tree/$', ConnectTree.as_view(req='tree'), name='connect_tree'),
    url(r'^connect/get-path/$', ConnectTree.as_view(req='path'), name='connect_path'),
    url(r'^connect/get-from-database/$', ConnectDatabase.as_view(), name='connect_database'),
    # url(r'^connect/(?P<rootid>.*)/(?P<modelid>.*)/$', ConnectTree.as_view(), name='connect_tree'),
    # library urls
    # url(r'^library/$', cache_page(10)(LibraryHomeView.as_view()), name='library_home'), #cache complete page
    url(r'^library/$', LibraryHomeView.as_view(), name='library_home'),
    url(r'^library/macro/$', LibraryMacroView.as_view(), name='library_macro'),
    url(r'^library/fast-search/', LibrarySearchView(), name='library_search'),
    url(r'^library/item:(?P<slug>[-_\w]+)/$', LibraryItemView.as_view(), name='library_item'),
    url(r'^library/item:(?P<slug>[-_\w]+)/list/$', LibraryExcerptView.as_view(), name='library_list'),
    url(r'^library/item:(?P<itemslug>[-_\w]+)/(?P<req_page>[^/]+)/$', LibraryPageView.as_view(), name='library_page'),
    url(r'^library/collection:(?P<slug>[-_\w]+)/$', LibraryCollectionView.as_view(), name='library_collection'),
    # notebooks urls
    url(r'^notebooks/$', NotebookHomeView.as_view(), name='notebooks_home'),
    url(r'^notebooks/fast-search/', NoteSearchView(), name='notebooks_fast_search'),
    url(r'^notebooks/item:(?P<noteb>.*[.]\d+[.]{1}?)/$', NotebookView.as_view(), name='notebooks_item'),
    url(r'^notebooks/item:(?P<noteb>.*[.]\d+[.]{1}?)/(?P<notebpage>.*[.]\d+[.][^/]+)/$', NotebookPageView.as_view(), name='notebooks_page'),
    # manuscripts urls
    url(r'^manuscripts/$', ManuscriptsHomeView.as_view(), name='manuscripts_home'),
    url(r'^manuscripts/fast-search/', ManuscriptsSearchView(), name='manuscripts_fast_search'),
    url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/$', ManuscriptCollectionView.as_view(target='detail', paginate_by=8), name='manuscripts_detail'),
    url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/list/$', ManuscriptCollectionView.as_view(target='pagelist'), name='manuscripts_pagelist'),
    url(r'^manuscripts/(?P<collectionslug>[-_\w]+)/(?P<manuscriptpage>[-_\w]+)/$', ManuscriptPageView.as_view(), name='manuscriptpage_detail'),
    # novels urls
    url(r'^novels/$', NovelsHomeView.as_view(), name='novels_home'),
    url(r'^novels/fast-search/', NovelsSearchView(), name='novels_fast_search'),
    url(r'^novels/(?P<novelslug>[-_\w]+)/$', NovelDetailView.as_view(), name='novel_detail'),
    url(r'^novels/(?P<novelslug>[-_\w]+)/(?P<novelpage>\d+)/$', NovelPageView.as_view(), name='novelpage_detail'),
)

# login
urlpatterns += [
    url('^', include('django.contrib.auth.urls'))
]

# admin
urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        )

# static/media config if Debug=True
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                            }),
                            )
