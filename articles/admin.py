# -*- coding: utf-8 -*-

from django.contrib import admin
from articles.models import Article, Section

class SectionInline(admin.TabularInline):
    model = Section

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('headline', 'slug', 'body', 'summary', 'tags', 'sections', 'author', 'photos')
        }),
        ('Publication', {
            'fields': ('pub_date', 'publish')
         }),
    )
    prepopulated_fields = {'slug': ('headline',)}
    list_display = ('headline', 'author', 'pub_date', 'publish')
    list_filter = ['pub_date', 'publish']
    

class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
