# -*- coding: utf-8 -*-

from django import forms
from articles.models import Article
from photologue.models import Photo
from django.contrib.auth.models import User

class SlugWidget(forms.TextInput):
    class Media:
        js = ('js/slug.js',)

class ArticleCreateForm(forms.ModelForm):
    slug = forms.CharField(widget=SlugWidget)
    class Meta:
        model = Article
        fields = ('headline', 'slug', 'summary', 'body') 
    class Media:
        css = {
            'all': ('css/forms.css',)
        }

class ArticleForm(forms.ModelForm):
    slug = forms.CharField(widget=SlugWidget)
    authors = forms.ModelMultipleChoiceField(queryset=User.objects.all().filter(is_staff=True))
    class Meta:
        model = Article
        fields = ('headline', 'slug', 'summary', 'body', 'tags', 'sections', 'authors', 'pub_ready') 
    class Media:
        css = {
            'all': ('css/forms.css',)
        }

class ArticleUpdatePublishedForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=User.objects.all().filter(is_staff=True))
    class Meta:
        model = Article
        fields = ('headline', 'summary', 'body', 'tags', 'sections', 'authors') 
    class Media:
        css = {
            'all': ('css/forms.css',)
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'crop_from', 'title', 'title_slug', 'caption', 'tags')
