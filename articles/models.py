# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from markdown2 import markdown
from tagging.fields import TagField
from tagging.models import Tag
from photologue.models import Photo

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def drafts(self):
        return self.filter(publish=False)

class Article(models.Model):
    headline = models.CharField('overskrift', max_length=200)
    slug = models.SlugField(unique_for_date="pub_date", help_text="en 'slug' er en URL-venlig titel til artiklen.")
    summary = models.TextField('resume', help_text="et kort resume eller introduktion til artiklen.")
    body = models.TextField("brødtekst", help_text="brug markdown formatering")
    body_html = models.TextField("rendered body text")
    sections = models.ManyToManyField('Section', related_name='articles', verbose_name="sektioner", blank=True)
    author = models.ForeignKey(User)
    photos = models.ManyToManyField(Photo, related_name='articles', null=True, blank=True)
    mod_date = models.DateTimeField(default=datetime.now)
    pub_date = models.DateTimeField("publicerings dato", default=datetime.now)
    publish = models.BooleanField("Publiceret på hjemmesiden", default=False,
                                  help_text='Artikler kan ikke ses på siden før deres "publicerings dato".')
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

class Section(models.Model):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles_section', args=[self.slug])
        

