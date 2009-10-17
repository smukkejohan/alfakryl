# -*- coding: utf-8 -*-

from datetime import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from articles.models import Article, Section
from tagging.models import Tag 
from articles.forms import ArticleForm

def section_archive(request, slug):
    section = get_object_or_404(Section, slug=slug)
    articles = Article.objects.published().filter(sections=section)
    
    return render_to_response(
        'articles/section_archive.html',
        {'articles': articles, 'section': section},
        context_instance = RequestContext(request)
    )
 
def tag_archive(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    articles = Article.objects.published().filter(tags=tag_id)
    
    return render_to_response(
        'articles/tag_archive.html',
        {'articles': articles, 'tag': tag},
        context_instance = RequestContext(request)
    )   

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
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = ArticleForm()
    return render_to_response(
        'articles/article_create.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
article_create = permission_required('articles.add_article')(article_create)

def article_update(request, article_id):
    """
    Renders a form for updating an existing article
    """
    a = Article.objects.get(pk=article_id)
    
    if not a.authors.all().get(pk=request.user.id):
        return HttpResponseForbidden("You don't have permissions to update this article.")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            
            request.user.message_set.create(message="Artiklen er blevet opdateret.")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = ArticleForm(instance=a)
    return render_to_response(
        'articles/article_update.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
article_update = permission_required('articles.change_article')(article_update)

def article_delete(request, article_id):
    """
    Renders a confirmation form, and deletes article upon post submission.
    """

    a = Article.objects.get(pk=article_id)
    
    if not a.authors.all().get(pk=request.user.id):
        return HttpResponseForbidden("You don't have permissions to delete this article.")
        
    if request.method == 'POST':
        a.delete()
        request.user.message_set.create(message="Artiklen er blevet slettet.")
        return HttpResponseRedirect(reverse('dashboard'))
        
    return render_to_response(
        'articles/article_delete.html',
        {'article': a},
        context_instance = RequestContext(request)
    )
article_delete = permission_required('articles.delete_article')(article_delete)
