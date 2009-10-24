# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.forms import UserProfileForm, UserForm, UserPortraitForm
from articles.models import Article

def profile(request, user):
    """
    Renders a profile for the given user if the user exists or returns 404.
    """
    
    user = get_object_or_404(User, username=user)   
    articles = Article.objects.published().filter(authors=user)
    
    return render_to_response(
        'profiles/profile.html', { 'object': user, 'articles': articles },
        context_instance = RequestContext(request)
    )

def update(request):
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = UserProfileForm(request.POST, instance=request.user.get_profile())
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            request.user.message_set.create(message="Ændringerne er blevet opdateret.")
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))  
    else:
        userform = UserForm(instance=request.user)
        try:
            profileform = UserProfileForm(instance=request.user.get_profile())
        except UserProfile.DoesNotExist:
            UserProfile(user=request.user).save()
            profileform = UserProfileForm(instance=request.user.get_profile())
    return render_to_response(
        'profiles/update.html', { 'userform': userform, 'profileform': profileform },
        context_instance = RequestContext(request)
    )

def portrait_upload(request):
    if request.method == 'POST':
        form = UserPortraitForm(request.POST, request.FILES, instance=request.user.userportrait)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Dit profilbillede er opdateret")
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))
    else:
        form = UserPortraitForm()
    
    return render_to_response(
        'profiles/portrait_upload.html', { 'form': form },
        context_instance = RequestContext(request)
    )
