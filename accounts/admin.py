# -*- coding: utf-8 -*-

from django.contrib import admin
from accounts.models import UserProfile, UserPortrait
from django.contrib.auth.models import User

class UserPortraitAdmin(admin.ModelAdmin):
        list_display = ['user', 'admin_thumbnail']

class UserProfileAdmin(admin.ModelAdmin):
        list_display = ['user']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPortrait, UserPortraitAdmin)
