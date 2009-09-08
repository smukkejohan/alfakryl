from datetime import datetime

from django.db import models
from django.conf import settings

from django.contrib.auth.models import User  

from tagging.fields import TagField
from tagging.models import Tag

class ArticleManager(models.Manager):
    def get_published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def get_drafts(self):
        return self.filter(publish=False)

class Article(models.Model):
    pub_date = models.DateTimeField("Publish date", default=datetime.now)
    headline = models.CharField(max_length=200)
    slug = models.SlugField(help_text='A "Slug" is a unique URL-friendly title for an object.')
    summary = models.TextField(help_text="A single paragraph summary or preview of the article.")
    body = models.TextField("Body text")
    author = models.ForeignKey(User)
    publish = models.BooleanField("Publish on site", default=True,
                                  help_text='Articles will not appear on the site until their "publish date".')
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    # Custom article manager
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('headline', 'author', 'pub_date', 'publish')
        list_filter = ['pub_date']
        save_as = True

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-article-detail', args=args)

