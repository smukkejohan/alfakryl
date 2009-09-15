# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from articles import views
from articles.models import Article

urlpatterns = patterns('',
    url(r'^create/$', views.article_create, name='article_create'),
    url(r'^update/(?P<article_id>\d)/$', views.article_update, name='article_update'),
    url(r'^myarticles/$', views.article_user_index, name='article_user_index'),
    #url(r'^preview/(?P<article_id>\d)/$', views.draft_preview, name='draft_preview'),
)

urlpatterns += patterns('django.views.generic.date_based',
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 
        'object_detail', {'queryset': Article.objects.published(), 
            'date_field': 'pub_date',
            'month_format': '%m'},
        name="article_detail"),

   #(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$', 
   #     'archive_day', info_dict),

   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        'archive_month', {'queryset': Article.objects.published(), 
            'date_field': 'pub_date',
            'month_format': '%m'},
        name="article_archive_month"),

   url(r'^(?P<year>\d{4})/$', 
        'archive_year', {'queryset': Article.objects.published(),
            'date_field': 'pub_date'},
        name="article_archive_year"),

   url(r'^$', 
        'archive_index', {'queryset': Article.objects.published(),
            'date_field': 'pub_date'},
        name="article_archive_index"),
)
