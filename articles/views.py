# -*- coding: utf-8 -*-

import random
from datetime import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from articles.models import Article, Section
from tagging.models import Tag 
from articles.forms import ArticleForm, ImageForm
from django.forms.models import modelformset_factory
from photologue.models import Photo


def section_archive(request, slug):
    section = get_object_or_404(Section, slug=slug)
    articles = Article.objects.published().filter(sections=section)
    
    return render_to_response(
        'articles/section_archive.html',
        {'object_list': articles, 'section': section},
        context_instance = RequestContext(request)
    )
 
def tag_archive(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    articles = Article.objects.published().filter(tags=tag_id)
    
    return render_to_response(
        'articles/tag_archive.html',
        {'object_list': articles, 'tag': tag},
        context_instance = RequestContext(request)
    )   

def random_article(request):
    """
    gets a random article, this might be a slow method, especially with man y articles 
    in the db, look into a better method.
    """
    article = Article.objects.published().order_by('?')[:1].get()
    return HttpResponseRedirect(article.get_absolute_url())

def article_detail(request, slug):
    """
    If the article is published return it and increment view count. 
    If it isn't check if its a draft and display it to authors and editors.
    Alternatively return permission denied.
    If its neither draft or public return does not exist.
    """  
    try:
        a = Article.objects.published().get(slug=slug)
        a.view_count += 1
        a.save()
        published = True
    except Article.DoesNotExist:
        try:
            a = Article.objects.drafts().get(slug=slug)
            published = False
            if not request.user.has_module_perms('articles'):
                return HttpResponseForbidden("This article is still a draft, if you are an author or editor you can log in to preview the article.")
        except Article.DoesNotExist:
            raise Http404
        
    return render_to_response(
        'articles/article_detail.html',
        {'object': a, 'published': published},
        context_instance = RequestContext(request)
    )

@login_required
def article_create(request):
    """
    Renders a form for creating a new article.
    """
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            article = form.save()
            article.authors.add(request.user)
            
            request.user.message_set.create(message="Din artikel er blevet gemt.")
            return HttpResponseRedirect(reverse('article_update', args=[article.id]))
    else:
        form = ArticleForm()
    return render_to_response(
        'articles/red/article_create.html',
        {'form': form},
        context_instance = RequestContext(request)
    )

@login_required
def article_update(request, article_id):
    """
    Renders a form for updating an existing article
    """
    a = get_object_or_404(Article, pk=article_id)
    
    if not request.user.is_superuser:
        try:
            a.authors.all().get(pk=request.user.id)
        except DoesNotExist:
            return HttpResponseForbidden("You don't have permissions to delete this article.")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=a)
        if form.is_valid():
            article = form.save()
            
            request.user.message_set.create(message="Artiklen er blevet opdateret.")
            return HttpResponseRedirect(article.get_absolute_url())
    else:
        form = ArticleForm(instance=a)
    return render_to_response(
        'articles/red/article_update.html',
        {'form': form},
        context_instance = RequestContext(request)
    )

@login_required
def article_delete(request, article_id):
    """
    Renders a confirmation form, and deletes article upon post submission.
    """

    a = get_object_or_404(Article, pk=article_id)
    
    if not request.user.is_superuser:
        try:
            a.authors.all().get(pk=request.user.id)
        except DoesNotExist:
            return HttpResponseForbidden("You don't have permissions to delete this article.")
        
    if request.method == 'POST':
        a.delete()
        request.user.message_set.create(message="Artiklen er blevet slettet.")
        return HttpResponseRedirect(reverse('dashboard'))
        
    return render_to_response(
        'articles/red/article_delete.html',
        {'article': a},
        context_instance = RequestContext(request)
    )

@login_required
def img_upload(request, article_id):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            article = get_object_or_404(Article, pk=article_id)
            img = form.save()
            article.photos.add(img)
            
            request.user.message_set.create(message="Billedet er blevet uploadet.")
            return HttpResponseRedirect(reverse('article_update', args=[article.id]))
    else:
        form = ImageForm()
    return render_to_response(
        'articles/red/img/upload.html',
        {'form': form},
        context_instance = RequestContext(request)
    )

@login_required
def img_update(request, img_id):
    img = get_object_or_404(Photo, pk=img_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=img)
       
        if form.is_valid():
            img = form.save()
            
            request.user.message_set.create(message="Billedet er blevet opdateret.")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = ImageForm(instance=img)
    return render_to_response(
        'articles/red/img/update.html',
        {'form': form},
        context_instance = RequestContext(request)
    )

@login_required
def img_delete(request, img_id):
    img = get_object_or_404(Photo, pk=img_id)
    if request.method == 'POST':
        img.delete()
        request.user.message_set.create(message="Billedet er blevet slettet.")
        return HttpResponseRedirect(reverse('dashboard'))
        
    return render_to_response(
        'articles/red/img/delete.html',
        {'img': img},
        context_instance = RequestContext(request)
    )
    
def manage_photos(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    PhotoFormSet = modelformset_factory(Photo)
    if request.method == "POST":
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = PhotoFormSet(queryset=Photo.objects.filter(articles=article_id))
    
    return render_to_response(
        'articles/red/img/manage.html',
        {'formset': formset, 'article': article},
        context_instance = RequestContext(request)
    )

