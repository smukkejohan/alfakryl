# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.models import User
from articles.models import Article

def index(request):
    articles = Article.objects.published()
    
    #try:
    #    primary_article = articles.filter(sections__title='Leder')[:1].get()
    #except:
    #    primary_article = articles[:1].get()
    #
    #articles = articles.exclude(pk=primary_article.id)
    
    return render_to_response(
        'index.html', {'articles': articles},
        context_instance = RequestContext(request)
    )

def dashboard(request):
    """
    render all drafts
    """
    
    articles = Article.objects.published()[:12]
    context = {'articles': articles}
    
    if request.user.has_module_perms('articles'):
        drafts = Article.objects.drafts()
        context.update({'drafts': drafts}) 
    
    return render_to_response(
        'dashboard.html', context,
        context_instance = RequestContext(request)
    )
# login required decorator

def user_profile(request, user):
    """
    Renders a profile for the given user if the user exists or returns 404.
    """
    
    user = get_object_or_404(User, username=user)   
    articles = Article.objects.published().filter(authors=u)
    
    return render_to_response(
        'user_profile.html', {'object': user, 'articles': articles },
        context_instance = RequestContext(request)
    )
