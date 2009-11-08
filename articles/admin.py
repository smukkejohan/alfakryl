# -*- coding: utf-8 -*-

from django.contrib import admin
from articles.models import Article, Section

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('headline', 'slug', 'body', 'summary', 'tags', 'sections', 'authors', 'layout')
        }),
        ('Publication', {
            'fields': ('pub_date', 'publish', 'pub_ready')
         }),
    )
    prepopulated_fields = {'slug': ('headline',)}
    list_display = ('headline', 'pub_date', 'publish', 'view_count')
    list_filter = ['pub_date', 'publish', 'pub_ready']
    

class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
