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
    year = models.IntegerField(max_length=4, null=True, blank=True)
    class_letter = models.CharField(max_length=2, null=True, blank=True)
    #school
    #url = models.URLField(null=True, blank=True)
    
    def save(self):
        self.class_letter = self.class_letter.upper()
        super(Article, self).save()

class UserPortrait(ImageModel):
    user = models.OneToOneField(User, primary_key=True)
    
