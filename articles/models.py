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
    slug = models.SlugField(unique=True, help_text="en 'slug' er en URL-venlig titel til artiklen.")
    summary = models.TextField('resume', help_text="Kort resume eller introduktion til artiklen.")
    #summary_html = models.TextField("rendered summary")
    body = models.TextField("brødtekst", help_text="Selve artiklen, du kan bruge markdown formatering.")
    body_html = models.TextField("rendered body")
    sections = models.ManyToManyField('Section', related_name='articles', verbose_name="sektioner", blank=True)
    authors = models.ManyToManyField(User, related_name='articles', verbose_name="forfattere", blank=True)
    photos = models.ManyToManyField(Photo, related_name='articles', null=True, blank=True)
    mod_date = models.DateTimeField(default=datetime.now)
    pub_date = models.DateTimeField("publicerings dato", default=datetime.now)
    publish = models.BooleanField("Publiceret", default=False,
                                  help_text='Artikler kan ikke ses på siden før deres "publicerings dato".')
    tags = TagField()
    view_count = models.IntegerField(default=0)
    #lix = models.IntegerField()
    pub_ready = models.BooleanField("Klar til publicering", default=False, help_text="Marker dette felt når artiklen er færdig og er klar til korrekturlæsning og publicering")
    
    
    
    objects = ArticleManager()
    
    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)
    
    def save(self, force_insert=False, force_update=False):
        """
        the body is only processed if it has changed
        
        """
        
        body_has_changed = False
        summary_has_changed = False
        new_instance = False
        
        if self.id:
            old = Article.objects.get(pk=self.id)
            
            if old.body != self.body:
                body_has_changed = True
            if old.summary != self.summary:
                summary_has_changed = True
            if body_has_changed or summary_has_changed or old.headline != self.headline:
                self.mod_date = datetime.now()
        else:
            new_instance = True
        
        if new_instance or body_has_changed: 
            self.body_html = markdown(self.body)
        
        if self.publish:
            self.pub_ready = True
        
        super(Article, self).save(force_insert, force_update)
        

    def __unicode__(self):
        return self.headline
    
    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', None, {
            'slug': self.slug
        })

class Section(models.Model):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    #menu_display = models.BooleanField('Hvis i hovedmenu', default=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('section_archive', args=[self.slug])
        
