# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from articles.models import Article
from articles.forms import ArticleForm

def article_user_index(request):
    user = request.user
    drafts = Article.objects.drafts().filter(author=user)
    articles = Article.objects.published().filter(author=user)
    
    return render_to_response(
        'articles/article_user_index.html', {'articles': articles, 'drafts': drafts },
        context_instance = RequestContext(request)
    )
article_user_index = permission_required('articles.can_add_article')(article_user_index)

def article_create(request):
    """
    Renders a form for creating a new article.
    """
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            
            request.user.message_set.create(message="Din artikel er blevet gemt.")
            return HttpResponseRedirect(reverse('article_user_index'))
    else:
        form = ArticleForm()
    return render_to_response(
        'articles/article_create.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
article_create = permission_required('articles.can_add_article')(article_create)

def article_update(request, article_id):
    """
    Renders a form for updating an existing article
    """
    a = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            
            request.user.message_set.create(message="Artiklen er blevet opdateret.")
            return HttpResponseRedirect(reverse('article_user_index'))
    else:
        form = ArticleForm(instance=a)
    return render_to_response(
        'articles/article_update.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
article_update = permission_required('articles.can_add_article')(article_update)

def article_delete(request, article_id):
    """
    Renders a confirmation form, and deletes article upon post submission.
    """
    permission = False
    a = Article.objects.get(pk=article_id)
    
    if a.author == request.user:
        permission = True
        if request.method == 'POST':
            a.delete()
            request.user.message_set.create(message="Artiklen er blevet slettet.")
            return HttpResponseRedirect(reverse('article_user_index'))
        
    return render_to_response(
        'articles/article_delete.html',
        {'article': a, 'permission': permission},
        context_instance = RequestContext(request)
    )
article_delete = permission_required('articles.can_delete_article')(article_delete)
