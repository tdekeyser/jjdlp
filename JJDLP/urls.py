from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
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
    url(r'^about/$', login_required(TemplateView.as_view(template_name='JJDLP/about.html')), name='about'),
    url(r'^bibliography/$', login_required(TemplateView.as_view(template_name='JJDLP/bibliography.html')), name='bibliography'),
    url(r'^stats/$', login_required(JJDLP.views.StatsView.as_view()), name='stats'),
    url(r'^docs/$', login_required(JJDLP.views.DocsView.as_view()), name='docs'),
    url(r'^docs/raw-markdown/$', login_required(JJDLP.views.DocsView.as_view(raw=True)), name='docs_raw_markdown'),
    url(r'^advanced-search/', login_required(JJDLP.views.AdvancedSearchView()), name='haystack_search'),
    url(r'^connect/$', login_required(JJDLP.views.ConnectView.as_view()), name='connect'),
    url(r'^connect/get-tree/$', login_required(JJDLP.views.ConnectTree.as_view(req='tree')), name='connect_tree'),
    url(r'^connect/get-path/$', login_required(JJDLP.views.ConnectTree.as_view(req='path')), name='connect_path'),
    # api
    url(r'^api/$', login_required(api.views.API.as_view()), name='connect_database'),
    # library urls
    url(r'^library/$', login_required(cache_page(60*1)(library.views.LibraryHomeView.as_view())), name='library_home'), #cache complete page
    # url(r'^library/$', library.views.LibraryHomeView.as_view(), name='library_home'),
    url(r'^library/fast-search/', login_required(library.views.LibrarySearchView()), name='library_search'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/list/$', login_required(library.views.LibraryExcerptView.as_view()), name='library_list'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/(?P<page>.+)/$', login_required(library.views.LibraryPageView.as_view()), name='library_page'),
    url(r'^library/(?P<collection>[-/_\w]+)/item:(?P<item>[-_\w]+)/$', login_required(library.views.LibraryItemView.as_view()), name='library_item'),
    url(r'^library/(?P<collection>[-/_\w]+)/$', login_required(library.views.LibraryCollectionView.as_view()), name='library_collection'),
    # notebooks urls
    url(r'^notebooks/$', login_required(notebooks.views.NotebookHomeView.as_view()), name='notebooks_home'),
    url(r'^notebooks/fast-search/', login_required(notebooks.views.NoteSearchView()), name='notebooks_fast_search'),
    # url(r'^notebooks/(?P<collection>[-/_\w]+)/nb:(?P<item>.*[.]\d+[.]{1}?)/(?P<page>.*[.]\d+[.][^/]+)/$', login_required(notebooks.views.NotebookPageView.as_view()), name='notebooks_page'),
    url(r'^notebooks/(?P<collection>[-/_\w]+)/(?P<item>.*[.]\d+[.]{1}?)/(?P<page>.+)/$', login_required(notebooks.views.NotebookPageView.as_view()), name='notebooks_page'),
    url(r'^notebooks/(?P<collection>[-/_\w]+)/(?P<item>.*[.]\d+[.]{1}?)/$', login_required(notebooks.views.NotebookView.as_view()), name='notebooks_item'),
    url(r'^notebooks/(?P<collection>[-/_\w]+)/$', login_required(notebooks.views.NotebookCollectionView.as_view()), name='notebooks_collection'),
    # manuscripts urls
    url(r'^manuscripts/$', login_required(manuscripts.views.ManuscriptsHomeView.as_view()), name='manuscripts_home'),
    url(r'^manuscripts/fast-search/', login_required(manuscripts.views.ManuscriptsSearchView()), name='manuscripts_fast_search'),
    url(r'^manuscripts/(?P<collection>[-_\w]+)/page:(?P<page>[-_\w]+)/$', login_required(manuscripts.views.ManuscriptPageView.as_view()), name='manuscripts_page'),
    url(r'^manuscripts/(?P<collection>[-_\w]+)/list/$', login_required(manuscripts.views.ManuscriptView.as_view(target='pagelist')), name='manuscripts_list'),
    url(r'^manuscripts/(?P<collection>[-_\w]+)/$', login_required(manuscripts.views.ManuscriptView.as_view(target='detail')), name='manuscripts_collection'),
    # novels urls
    url(r'^texts/$', login_required(texts.views.TextsHomeView.as_view()), name='texts_home'),
    url(r'^texts/fast-search/', login_required(texts.views.TextsSearchView()), name='texts_fast_search'),
    url(r'^texts/(?P<slug>[-_\w]+)/$', login_required(texts.views.TextView.as_view()), name='texts_item'),
    url(r'^texts/(?P<slug>[-_\w]+)/(?P<page>\d+)/$', login_required(texts.views.TextPageView.as_view()), name='texts_page'),

    # login pages
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
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
        url(r'^media/(?P<path>.*)$', login_required('django.views.static.serve'), {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', login_required('django.views.static.serve'), {
            'document_root': settings.STATIC_ROOT,
        }),
        )
