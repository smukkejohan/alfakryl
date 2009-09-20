# -*- coding: utf-8 -*-

from django import forms
from articles.models import Article
 
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'slug', 'summary', 'body', 'tags', 'sections')
