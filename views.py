# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.models import User
from articles.models import Article

def index(request):
    pass

def user_profile(request, user):
    """
    Renders a profile for the given user if the user exists or returns 404.
    """
    
    u = get_object_or_404(User, username=user)
    
    #if request.user.has_perms('')
    
    #drafts = Article.objects.drafts().filter(author=u)  
    
    articles = Article.objects.published().filter(author=u)
    
    return render_to_response(
        'user_profile.html', {'articles': articles, 'user': u },
        context_instance = RequestContext(request)
    )
