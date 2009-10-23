# -*- coding: utf-8 -*-

from django.contrib import admin
from accounts.models import UserProfile, UserPortrait

class UserPortraitAdmin(admin.ModelAdmin):
        list_display = ['user', 'admin_thumbnail']


admin.site.register(UserProfile)
admin.site.register(UserPortrait, UserPortraitAdmin)
