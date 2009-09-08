from django.contrib import admin
from alfakrol.ink.models import Article

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('headline', 'slug', 'body', 'summary')
        }),
        (None, {
            'fields': ('author',)
        }),
        ('Publish', {
            'classes': ('collapse',),
            'fields': ('pub_date', 'publish')
         }),
    )

admin.site.register(Article, ArticleAdmin)
