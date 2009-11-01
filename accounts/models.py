# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from datetime import datetime
from photologue.models import ImageModel

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    bio = models.TextField(null=True, blank=True)
    facebook = models.CharField(null=True, blank=True, max_length=56)
    twitter = models.CharField(null=True, blank=True, max_length=56)
    year = models.IntegerField("årgang", max_length=4, null=True, blank=True, help_text="Det år du bliver student.")
    class_letter = models.CharField("Klasse bogstav", max_length=2, null=True, blank=True, help_text="Skriv kun bogstavet og ikke din årgang.")
    job = models.CharField(null=True, blank=True, max_length=128)
    #school
    #url = models.URLField(null=True, blank=True)
    
    def save(self):
        #self.class_letter = ''.join(self.class_letter).upper()
        super(UserProfile, self).save()

class UserPortrait(ImageModel):
    user = models.OneToOneField(User, primary_key=True)
    
