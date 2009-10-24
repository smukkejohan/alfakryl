# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = patterns('',
    url(r'^update/$', views.update, name='profile_update'),
    url(r'^update-portrait/$', views.portrait_upload, name='user_portrait_upload'),
    url(r'^(?P<user>[-\w]+)/$', views.profile, name='user_profile'),
)
