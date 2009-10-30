# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.models import User, Group
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

def redaktionen(request):
    staff = User.objects.all().filter(is_staff=True, is_active=True)
    
    return render_to_response(
        'redaktionen.html', {'writers': staff},
        context_instance = RequestContext(request)
    )
    

