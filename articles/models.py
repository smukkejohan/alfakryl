# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.conf import settings
from markdown2 import markdown
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def drafts(self):
        return self.filter(publish=False)

class Article(models.Model):
    headline = models.CharField('overskrift', max_length=200)
    slug = models.SlugField(help_text="en 'slug' er en URL-venlig titel til artiklen.")
    summary = models.TextField('resume', help_text="Et kort resume eller introduktion til artiklen.")
    body = models.TextField("brødtekst", help_text="brug markdown formatering")
    body_html = models.TextField("rendered body text")
    author = models.ForeignKey(User)
    mod_date = models.DateTimeField(default=datetime.now)
    pub_date = models.DateTimeField("Publish date", default=datetime.now)
    publish = models.BooleanField("Publish on site", default=False,
                                  help_text='Articles will not appear on the site until their "publish date".')
    tags = TagField()
    
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)
    
    def save(self):
        self.mod_date = datetime.now()
        self.body_html = markdown(self.body)
        super(Article, self).save()

    def __unicode__(self):
        return self.headline

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', None, {
            'year': self.pub_date.year,
            'month': self.pub_date.month,
            'day': self.pub_date.day,
            'slug': self.slug
        })

