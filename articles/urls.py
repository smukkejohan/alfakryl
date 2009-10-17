# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from articles import views
from articles.models import Article

urlpatterns = patterns('',
    url(r'^create/$', views.article_create, name='article_create'),
    url(r'^update/(?P<article_id>\d+)/$', views.article_update, name='article_update'),
    url(r'^delete/(?P<article_id>\d+)/$', views.article_delete, name='article_delete'),
    url(r'^(?P<slug>[-\w]+)/$', views.article_detail, name='article_detail'),
    url(r'^section/(?P<slug>[-\w]+)/$', views.section_archive, name='section_archive'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.tag_archive, name='tag_archive'),
    
)

urlpatterns += patterns('django.views.generic.date_based',

#(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$', 
#     'archive_day', info_dict),

   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        'archive_month', {'queryset': Article.objects.published(), 
            'date_field': 'pub_date',
            'month_format': '%m'},
        name="article_archive_month"),

#   url(r'^(?P<year>\d{4})/$', 
#        'archive_year', {'queryset': Article.objects.published(),
#            'date_field': 'pub_date'},
#        name="article_archive_year"),

#   url(r'^$', 
#        'archive_index', {'queryset': Article.objects.published(),
#            'date_field': 'pub_date'},
#        name="article_archive_index"),
)
