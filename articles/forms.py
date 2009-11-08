# -*- coding: utf-8 -*-

from django import forms
from articles.models import Article
from photologue.models import Photo
from django.contrib.auth.models import User
 

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'slug', 'summary', 'body', 'tags', 'sections', 'authors', 'pub_ready')
        authors = forms.ModelMultipleChoiceField(queryset=User.objects.all().filter(is_staff=True))

class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'crop_from', 'title', 'title_slug', 'caption', 'tags')
