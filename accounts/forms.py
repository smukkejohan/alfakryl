# -*- coding: utf-8 -*-

from django import forms
from accounts.models import UserProfile, UserPortrait
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'facebook', 'twitter', 'year', 'class_letter',)

class UserPortraitForm(forms.ModelForm):
    class Meta:
        model = UserPortrait
        fields = ('image', 'crop_from')
