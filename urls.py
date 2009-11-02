# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from articles.feeds import LatestArticles, LatestArticlesBySection

feeds = {
    'latest': LatestArticles,
    'sections': LatestArticlesBySection,
}

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    (r'^photos/', include('photologue.urls')),   
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^accounts/', include('registration.urls')),
    (r'^p/', include('accounts.urls')),
    (r'^a/', include('alfakryl.articles.urls')),
    url(r'^$', 'views.index', name='main_index'),
    url(r'^redaktionen/$', 'views.redaktionen', name='redaktionen'),
    url(r'^dashboard/$', 'views.dashboard', name='dashboard'),

    #url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', 
        #{'sitemaps': sitemaps}, name='sitemap'),
    #rss
    #url(r'^robots.txt', '')
)

if settings.DEVELOPMENT_MODE:
    urlpatterns += patterns('django.views',
        url(r'%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
    )
