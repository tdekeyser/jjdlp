from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.decorators.cache import cache_page
# from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, RedirectView

import JJDLP.views
import api.views
import library.views
import notebooks.views
import manuscripts.views
import texts.views

# static solely for developement:
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='JJDLP/base.html'), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/JJDLP/images/favicon.ico', permanent=True)),
    url(r'^about/$', TemplateView.as_view(template_name='JJDLP/about.html'), name='about'),
    url(r'^bibliography/$', TemplateView.as_view(template_name='JJDLP/bibliography.html'), name='bibliography'),
    url(r'^stats/$', JJDLP.views.StatsView.as_view(), name='stats'),
    url(r'^docs/$', JJDLP.views.DocsView.as_view(), name='docs'),
    url(r'^docs/raw-markdown/$', JJDLP.views.DocsView.as_view(raw=True), name='docs_raw_markdown'),
    url(r'^advanced-search/', JJDLP.views.AdvancedSearchView(), name='haystack_search'),
    url(r'^connect/$', JJDLP.views.ConnectView.as_view(), name='connect'),
    url(r'^connect/get-tree/$', JJDLP.views.ConnectTree.as_view(req='tree'), name='connect_tree'),
    url(r'^connect/get-path/$', JJDLP.views.ConnectTree.as_view(req='path'), name='connect_path'),
    # api
    url(r'^api/$', api.views.API.as_view(), name='connect_database'),
    # library urls
    url(r'^library/$', cache_page(60*1, key_prefix='libhome')(library.views.LibraryHomeView.as_view()), name='library_home'), #cache complete page
    # url(r'^library/$', library.views.LibraryHomeView.as_view(), name='library_home'),
    url(r'^library/fast-search/', library.views.LibrarySearchView(), name='library_search'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/list/$', library.views.LibraryExcerptView.as_view(), name='library_list'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/(?P<page>.+)/$', library.views.LibraryPageView.as_view(), name='library_page'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/$', library.views.LibraryItemView.as_view(), name='library_item'),
    url(r'^library/(?P<collection>[-/_\w]+)/$', library.views.LibraryCollectionView.as_view(), name='library_collection'),
    # notebooks urls
    url(r'^notebooks/$', notebooks.views.NotebookHomeView.as_view(), name='notebooks_home'),
    url(r'^notebooks/fast-search/', notebooks.views.NoteSearchView(), name='notebooks_fast_search'),
    url(r'^notebooks/(?P<noteb>.*[.]\d+[.]{1}?)/$', notebooks.views.NotebookView.as_view(), name='notebooks_item'),
    url(r'^notebooks/(?P<noteb>.*[.]\d+[.]{1}?)/(?P<notebpage>.*[.]\d+[.][^/]+)/$', notebooks.views.NotebookPageView.as_view(), name='notebooks_page'),
    # manuscripts urls
    url(r'^manuscripts/$', manuscripts.views.ManuscriptsHomeView.as_view(), name='manuscripts_home'),
    url(r'^manuscripts/fast-search/', manuscripts.views.ManuscriptsSearchView(), name='manuscripts_fast_search'),
    url(r'^manuscripts/collection-(?P<slug>[-_\w]+)/$', manuscripts.views.ManuscriptCollectionView.as_view(target='detail', paginate_by=8), name='manuscripts_item'),
    url(r'^manuscripts/collection-(?P<slug>[-_\w]+)/list/$', manuscripts.views.ManuscriptCollectionView.as_view(target='pagelist'), name='manuscripts_list'),
    url(r'^manuscripts/collection-(?P<slug>[-_\w]+)/(?P<page>[-_\w]+)/$', manuscripts.views.ManuscriptPageView.as_view(), name='manuscripts_page'),
    # novels urls
    url(r'^texts/$', texts.views.NovelsHomeView.as_view(), name='texts_home'),
    url(r'^texts/fast-search/', texts.views.NovelsSearchView(), name='texts_fast_search'),
    url(r'^texts/(?P<slug>[-_\w]+)/$', texts.views.NovelView.as_view(), name='texts_item'),
    url(r'^texts/(?P<slug>[-_\w]+)/(?P<page>\d+)/$', texts.views.NovelPageView.as_view(), name='texts_page'),
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
