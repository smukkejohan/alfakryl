from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from datetime import datetime
from photologue.models import ImageModel

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    portrait = models.ForeignKey(UserPortrait, null=True)
    bio = models.TextField(null=True)
    facebook = models.CharField(null=True)
    twitter = models.CharField(null=True)
    #year = models.
    #school
    #letter
    url = models.UrlField(null=True)

class UserPortrait(ImageModel):
